"""Giao diện dòng lệnh: python -m pomodoro --work 25 --short 5 --long 15"""
import argparse
import sys
import time

from .config import LABELS, Config, Phase
from .energy import LEVELS, suggest_break
from .session import Session
from .timer import CountdownTimer, format_mmss


def run_phase(phase: Phase, minutes: int) -> str:
    """Chạy một phiên. Trả về 'done' | 'aborted' | 'quit'."""
    timer = CountdownTimer(minutes * 60)
    timer.start()
    label = LABELS[phase]
    try:
        while not timer.finished():
            print(f"\r[{label}] {format_mmss(timer.remaining())}  ", end="", flush=True)
            time.sleep(0.2)
    except KeyboardInterrupt:
        timer.pause()
        print()
        while True:
            c = input("Tạm dừng. [c] tiếp tục, [r] hủy phiên, [q] thoát: ").strip().lower()
            if c == "c":
                timer.start()
                return _resume(timer, label)
            if c == "r":
                return "aborted"
            if c == "q":
                return "quit"
    print(f"\r[{label}] 00:00  \a")
    return "done"


def _resume(timer: CountdownTimer, label: str) -> str:
    try:
        while not timer.finished():
            print(f"\r[{label}] {format_mmss(timer.remaining())}  ", end="", flush=True)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print()
        return "aborted"
    print(f"\r[{label}] 00:00  \a")
    return "done"


def ask_energy() -> int:
    print("Mức năng lượng của bạn lúc này?")
    for k, v in LEVELS.items():
        print(f"  {k}. {v}")
    while True:
        raw = input("Chọn 1-5 (mặc định 3): ").strip() or "3"
        if raw in {"1", "2", "3", "4", "5"}:
            return int(raw)
        print("Vui lòng nhập số từ 1 đến 5.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pomodoro", description="Đồng hồ Pomodoro 25/5")
    p.add_argument("--work", type=int, default=25, help="phút học (15-60)")
    p.add_argument("--short", type=int, default=5, help="phút nghỉ ngắn (3-10)")
    p.add_argument("--long", type=int, default=15, help="phút nghỉ dài (15-30)")
    p.add_argument("--cycle", type=int, default=4, help="số phiên trước khi nghỉ dài")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cfg = Config(work=args.work, short=args.short, long=args.long, cycle=args.cycle)
    except ValueError as e:
        print(f"Lỗi cấu hình: {e}", file=sys.stderr)
        return 2

    session = Session(cfg)
    print("Pomodoro CLI. Nhấn Ctrl+C để tạm dừng.")
    while True:
        input(f"\nNhấn Enter để bắt đầu phiên học {cfg.work} phút... ")
        result = run_phase(Phase.WORK, cfg.work)
        if result == "quit":
            break
        if result == "aborted":
            print("Phiên bị hủy, không được tính là một Pomodoro.")
            session.abort_work()
            continue

        default_phase = session.complete_work()
        print(f"Hoàn thành! Hôm nay: {session.total} Pomodoro, chu kỳ {session.cycle}/{cfg.cycle}.")
        s = suggest_break(ask_energy(), long_due=session.long_due())
        print(f"Gợi ý: {LABELS[s.phase].lower()} {s.minutes} phút. {s.reason}")
        pick = input("Enter = nhận gợi ý, d = nghỉ mặc định: ").strip().lower()
        if pick == "d":
            phase, minutes = default_phase, cfg.minutes_for(default_phase)
        else:
            phase, minutes = s.phase, s.minutes

        result = run_phase(phase, minutes)
        if result == "quit":
            break
        session.finish_break(phase)
    print("Tạm biệt!")
    return 0
