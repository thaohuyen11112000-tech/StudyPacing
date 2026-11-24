
import csv
import os
import struct
import zlib


def export_csv_ac1(rows: list[list[str]], output_path: str = "ac1_sample.csv") -> str:
    """AC1: Tạo file .csv hỗ trợ tiếng Việt có dấu (utf-8-sig) không lỗi font."""
    parent_dir = os.path.dirname(output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(output_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    return os.path.abspath(output_path)


def _find_vietnamese_ttf(custom_font_path: str | None = None) -> str:
    """Tìm font .ttf hỗ trợ tiếng Việt trên máy."""
    candidates = [
        custom_font_path,
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\DejaVuSans.ttf",
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    raise FileNotFoundError("Không tìm thấy file font .ttf hỗ trợ tiếng Việt.")


def _parse_ttf_cmap(ttf_bytes: bytes) -> tuple[dict[int, int], list[int], tuple[int, int, int, int], int]:
    """Đọc bảng ánh xạ Unicode sang Glyph ID từ file font .ttf."""
    num_tables = struct.unpack(">H", ttf_bytes[4:6])[0]
    tables: dict[str, bytes] = {}
    for i in range(num_tables):
        off = 12 + i * 16
        tag = ttf_bytes[off : off + 4].decode("latin1")
        t_off, t_len = struct.unpack(">II", ttf_bytes[off + 8 : off + 16])
        tables[tag] = ttf_bytes[t_off : t_off + t_len]

    head = tables["head"]
    units_per_em = struct.unpack(">H", head[18:20])[0]
    x_min, y_min, x_max, y_max = struct.unpack(">hhhh", head[36:44])

    hhea = tables["hhea"]
    num_hmetrics = struct.unpack(">H", hhea[34:36])[0]

    hmtx = tables["hmtx"]
    glyph_widths: list[int] = []
    last_w = 500
    for i in range(num_hmetrics):
        w = struct.unpack(">H", hmtx[i * 4 : i * 4 + 2])[0]
        last_w = int(round(w * 1000.0 / units_per_em))
        glyph_widths.append(last_w)

    maxp = tables["maxp"]
    num_glyphs = struct.unpack(">H", maxp[4:6])[0]
    while len(glyph_widths) < num_glyphs:
        glyph_widths.append(last_w)

    cmap = tables["cmap"]
    num_subtables = struct.unpack(">H", cmap[2:4])[0]
    sub_off = None
    sub_fmt = None
    for i in range(num_subtables):
        off = 4 + i * 8
        pid, eid, s_off = struct.unpack(">HHI", cmap[off : off + 8])
        fmt = struct.unpack(">H", cmap[s_off : s_off + 2])[0]
        if (pid, eid) in ((3, 10), (0, 4)) and fmt == 12:
            sub_off, sub_fmt = s_off, 12
            break
        if (pid, eid) in ((3, 1), (0, 3)) and fmt == 4:
            sub_off, sub_fmt = s_off, 4

    uni_to_gid: dict[int, int] = {}
    if sub_fmt == 12:
        n_groups = struct.unpack(">I", cmap[sub_off + 12 : sub_off + 16])[0]
        for g in range(n_groups):
            g_off = sub_off + 16 + g * 12
            sc, ec, sgid = struct.unpack(">III", cmap[g_off : g_off + 12])
            for code in range(sc, min(ec + 1, 0x10000)):
                uni_to_gid[code] = sgid + (code - sc)
    elif sub_fmt == 4:
        seg_cnt = struct.unpack(">H", cmap[sub_off + 6 : sub_off + 8])[0] // 2
        end_codes = struct.unpack(f">{seg_cnt}H", cmap[sub_off + 14 : sub_off + 14 + 2 * seg_cnt])
        start_base = sub_off + 16 + 2 * seg_cnt
        start_codes = struct.unpack(f">{seg_cnt}H", cmap[start_base : start_base + 2 * seg_cnt])
        delta_base = start_base + 2 * seg_cnt
        id_deltas = struct.unpack(f">{seg_cnt}h", cmap[delta_base : delta_base + 2 * seg_cnt])
        range_base = delta_base + 2 * seg_cnt
        id_range_offsets = struct.unpack(f">{seg_cnt}H", cmap[range_base : range_base + 2 * seg_cnt])

        for i in range(seg_cnt):
            sc, ec, delta, ro = start_codes[i], end_codes[i], id_deltas[i], id_range_offsets[i]
            if sc == 0xFFFF:
                continue
            for code in range(sc, ec + 1):
                if ro == 0:
                    gid = (code + delta) & 0xFFFF
                else:
                    g_idx_off = range_base + i * 2 + ro + (code - sc) * 2
                    gid = struct.unpack(">H", cmap[g_idx_off : g_idx_off + 2])[0]
                    if gid != 0:
                        gid = (gid + delta) & 0xFFFF
                if gid != 0:
                    uni_to_gid[code] = gid

    bbox = (
        int(round(x_min * 1000.0 / units_per_em)),
        int(round(y_min * 1000.0 / units_per_em)),
        int(round(x_max * 1000.0 / units_per_em)),
        int(round(y_max * 1000.0 / units_per_em)),
    )
    return uni_to_gid, glyph_widths, bbox, num_glyphs


def export_pdf_ac1(
    lines: list[str],
    output_path: str = "ac1_sample.pdf",
    font_path: str | None = None,
) -> str:
    """AC1: Tạo file .pdf có nhúng font tiếng Việt để hiển thị dấu rõ ràng, không lỗi font."""
    resolved_font = _find_vietnamese_ttf(font_path)
    with open(resolved_font, "rb") as f:
        ttf_bytes = f.read()

    uni_to_gid, glyph_widths, bbox, num_glyphs = _parse_ttf_cmap(ttf_bytes)

    used_gids: dict[int, int] = {}
    ops = ["BT"]
    y = 780
    for line in lines:
        if not line:
            y -= 12
            continue
        hex_gids = []
        for ch in line:
            gid = uni_to_gid.get(ord(ch), 0)
            used_gids[gid] = ord(ch)
            hex_gids.append(f"{gid:04X}")
        ops.append("/F1 12 Tf")
        ops.append(f"1 0 0 1 50 {y} Tm")
        ops.append(f"<{''.join(hex_gids)}> Tj")
        y -= 20
        if y < 60:
            break
    ops.append("ET")
    stream_data = "\n".join(ops).encode("ascii")

    bf_lines = [f"<{gid:04X}> <{code:04X}>" for gid, code in sorted(used_gids.items()) if code > 0]
    tounicode = (
        "/CIDInit /ProcSet findresource begin\n"
        "12 dict begin begincmap\n"
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
        "/CMapName /Adobe-Identity-UCS def /CMapType 2 def\n"
        "1 begincodespacerange <0000> <FFFF> endcodespacerange\n"
        f"{len(bf_lines)} beginbfchar\n"
        + "\n".join(bf_lines)
        + "\nendbfchar\nendcmap CMapName currentdict /CMap defineresource pop end end"
    ).encode("ascii")

    w_items = [f"{gid} [{glyph_widths[gid]}]" for gid in sorted(used_gids.keys()) if gid < len(glyph_widths)]
    w_arr = "[" + " ".join(w_items) + "]"
    comp_ttf = zlib.compress(ttf_bytes)

    cid_map = bytearray(num_glyphs * 2)
    for gid in range(num_glyphs):
        cid_map[gid * 2 : gid * 2 + 2] = struct.pack(">H", gid)
    comp_cid = zlib.compress(bytes(cid_map))

    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type0 /BaseFont /AC1VNFont "
        b"/Encoding /Identity-H /DescendantFonts [6 0 R] /ToUnicode 9 0 R >>",
        f"<< /Length {len(stream_data)} >>\nstream\n".encode("ascii") + stream_data + b"\nendstream",
        f"<< /Type /Font /Subtype /CIDFontType2 /BaseFont /AC1VNFont "
        f"/CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> "
        f"/FontDescriptor 7 0 R /W {w_arr} /CIDToGIDMap 10 0 R >>".encode("ascii"),
        f"<< /Type /FontDescriptor /FontName /AC1VNFont /Flags 32 "
        f"/FontBBox [{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}] /ItalicAngle 0 "
        f"/Ascent 900 /Descent -200 /CapHeight 700 /StemV 80 /FontFile2 8 0 R >>".encode("ascii"),
        f"<< /Length {len(comp_ttf)} /Length1 {len(ttf_bytes)} /Filter /FlateDecode >>\nstream\n".encode("ascii")
        + comp_ttf
        + b"\nendstream",
        f"<< /Length {len(tounicode)} >>\nstream\n".encode("ascii") + tounicode + b"\nendstream",
        f"<< /Length {len(comp_cid)} /Filter /FlateDecode >>\nstream\n".encode("ascii")
        + comp_cid
        + b"\nendstream",
    ]

    parent_dir = os.path.dirname(output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    pdf_bytes = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for idx, obj in enumerate(objs, start=1):
        offsets.append(len(pdf_bytes))
        pdf_bytes.extend(f"{idx} 0 obj\n".encode("ascii"))
        pdf_bytes.extend(obj)
        pdf_bytes.extend(b"\nendobj\n")

    xref_pos = len(pdf_bytes)
    pdf_bytes.extend(f"xref\n0 {len(objs) + 1}\n".encode("ascii"))
    pdf_bytes.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf_bytes.extend(f"{off:010d} 00000 n \n".encode("ascii"))

    pdf_bytes.extend(
        f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )

    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    return os.path.abspath(output_path)
    

