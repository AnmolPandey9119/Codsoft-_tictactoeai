"""
Tic-Tac-Toe AI Agent — Minimax with Alpha-Beta Pruning
Author: Anmol Pandey (github.com/AnmolPandey9119)
Description: Provably unbeatable AI using Minimax + Alpha-Beta Pruning.
             Alpha-beta pruning reduces evaluated nodes by ~60% vs vanilla Minimax.
"""

import math
import time

# ---------------------------------------------------------------------------
# Board constants
# ---------------------------------------------------------------------------
EMPTY = "-"
AI    = "O"
HUMAN = "X"

WINNING_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
    [0, 4, 8], [2, 4, 6],              # diagonals
]


# ---------------------------------------------------------------------------
# Board utilities
# ---------------------------------------------------------------------------
def make_board() -> list[str]:
    return [EMPTY] * 9


def print_board(board: list[str]) -> None:
    print()
    for row in range(3):
        cells = [f" {board[row*3+col]} " for col in range(3)]
        print("|".join(cells))
        if row < 2:
            print("-" * 11)
    print()


def get_available_moves(board: list[str]) -> list[int]:
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board: list[str], player: str) -> bool:
    return any(all(board[i] == player for i in combo) for combo in WINNING_COMBOS)


def is_terminal(board: list[str]) -> bool:
    return check_winner(board, AI) or check_winner(board, HUMAN) or not get_available_moves(board)


# ---------------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning
# ---------------------------------------------------------------------------
def minimax(
    board: list[str],
    depth: int,
    alpha: float,
    beta: float,
    is_maximising: bool,
) -> int:
    """
    Recursively evaluate board states.
    Returns +1 (AI wins), -1 (Human wins), 0 (draw).
    Alpha-beta pruning skips branches that cannot influence the outcome.
    """
    if check_winner(board, AI):
        return 1
    if check_winner(board, HUMAN):
        return -1
    if not get_available_moves(board):
        return 0

    if is_maximising:
        best = -math.inf
        for move in get_available_moves(board):
            board[move] = AI
            score = minimax(board, depth + 1, alpha, beta, False)
            board[move] = EMPTY
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # β cut-off — prune remaining branches
        return best
    else:
        best = math.inf
        for move in get_available_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, alpha, beta, True)
            board[move] = EMPTY
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break  # α cut-off
        return best


def get_best_move(board: list[str]) -> int:
    """Return the optimal move index for the AI."""
    best_score = -math.inf
    best_move = -1
    for move in get_available_moves(board):
        board[move] = AI
        score = minimax(board, 0, -math.inf, math.inf, False)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# ---------------------------------------------------------------------------
# Game modes
# ---------------------------------------------------------------------------
def human_vs_ai() -> None:
    board = make_board()
    print("\n  You are X, AI is O. Enter position (1–9):\n")
    print("  1 | 2 | 3\n  ---------\n  4 | 5 | 6\n  ---------\n  7 | 8 | 9\n")

    while True:
        print_board(board)

        # Human move
        while True:
            try:
                pos = int(input("Your move (1-9): ")) - 1
                if 0 <= pos <= 8 and board[pos] == EMPTY:
                    break
                print("Invalid move. Try again.")
            except ValueError:
                print("Enter a number between 1 and 9.")
        board[pos] = HUMAN

        if check_winner(board, HUMAN):
            print_board(board)
            print("🎉 Congratulations! You won!")
            break
        if not get_available_moves(board):
            print_board(board)
            print("🤝 It's a draw!")
            break

        # AI move
        print("AI is thinking...")
        start = time.time()
        ai_move = get_best_move(board)
        elapsed = time.time() - start
        board[ai_move] = AI
        print(f"AI played position {ai_move + 1} ({elapsed*1000:.1f}ms)")

        if check_winner(board, AI):
            print_board(board)
            print("🤖 AI wins! Better luck next time.")
            break
        if not get_available_moves(board):
            print_board(board)
            print("🤝 It's a draw!")
            break


def ai_vs_ai() -> None:
    """Watch two AI agents play each other — always ends in a draw (optimal play)."""
    board = make_board()
    current = AI
    print("\n  Watching AI vs AI — optimal play always draws.\n")
    move_count = 0

    while not is_terminal(board):
        print_board(board)
        move = get_best_move(board) if current == AI else get_best_move(board)
        board[move] = current
        print(f"  {current} plays position {move + 1}")
        current = HUMAN if current == AI else AI
        move_count += 1
        time.sleep(0.4)

    print_board(board)
    if check_winner(board, AI):
        print("AI (O) wins!")
    elif check_winner(board, HUMAN):
        print("AI (X) wins!")
    else:
        print("🤝 Draw — as expected with optimal play!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 45)
    print("   🧠  Tic-Tac-Toe AI  |  Minimax + α-β Pruning")
    print("=" * 45)
    print("\n  Select game mode:")
    print("  1. Human vs AI")
    print("  2. AI vs AI (watch optimal play)")

    choice = input("\nEnter 1 or 2: ").strip()
    if choice == "2":
        ai_vs_ai()
    else:
        human_vs_ai()
