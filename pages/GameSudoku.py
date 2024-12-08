import streamlit as st
import numpy as np
import time
from module import js_test

st.set_page_config(page_title="Sudoku Game", page_icon="🧩", layout="centered")

# CSS 스타일 정의
st.markdown(
    """
    <style>
    .st-key-chat {
        position: fixed;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 스도쿠 유효성 검사
def check_valid(board, row, col, num):
    for c in range(9):
        if c != col and board[row][c] == num:
            return False
    for r in range(9):
        if r != row and board[r][col] == num:
            return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if (box_row + i != row or box_col + j != col) and board[box_row + i][box_col + j] == num:
                return False
    return True

# 스도쿠 보드 생성
def create_sudoku_board(difficulty=0.5):
    board = np.zeros((9, 9), dtype=int)
    def fill_board(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    nums = np.random.permutation(range(1, 10))
                    for num in nums:
                        if check_valid(board, row, col, num):
                            board[row][col] = num
                            if fill_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    fill_board(board)
    num_to_remove = int(difficulty * 81)
    coords = [(r, c) for r in range(9) for c in range(9)]
    np.random.shuffle(coords)
    for r, c in coords[:num_to_remove]:
        board[r][c] = 0
    return board

# 오류 위치를 체크하여 틀린 개수 반환하는 함수
def get_invalid_count(board, original_board):
    invalid_positions = set()  # 잘못된 위치를 기록

    for i in range(9):
        for j in range(9):
            if original_board[i, j] == 0 and board[i, j] != 0:  # 입력된 칸만 체크
                num = board[i, j]

                # 해당 숫자가 유효하지 않으면 위치를 추가
                if not check_valid(board, i, j, num):
                    invalid_positions.add((i, j))

    return len(invalid_positions)

# 점수 계산 함수
def calculate_score(difficulty, elapsed_time):
    difficulty_base_scores = {1: 300, 2: 500, 3: 700, 4: 850, 5: 1000}
    base_score = difficulty_base_scores.get(difficulty, 700)
    target_times = {1: 180, 2: 240, 3: 300, 4: 420, 5: 600}
    target_time = target_times.get(difficulty, 300)

    if elapsed_time <= target_time:
        time_bonus = base_score * 0.2 * (1 - elapsed_time / target_time)
        final_score = int(base_score + time_bonus)
    else:
        time_penalty = base_score * 0.5 * ((elapsed_time - target_time) / target_time)
        final_score = int(max(base_score * 0.5, base_score - time_penalty))

    return max(0, final_score)

# 메인 함수
def main():
    st.title("🧩 스도쿠 게임")
    st.write("각 행, 열, 3x3 박스에 1-9 숫자가 중복되지 않도록 채워주세요!")

    # 게임 초기화
    if 'board' not in st.session_state:
        st.session_state.board = create_sudoku_board()
        st.session_state.original_board = st.session_state.board.copy()
        st.session_state.invalid_positions = []
        st.session_state.start_time = time.time()

    # 난이도 설정
    difficulty_levels = 5
    difficulty_step = 0.5 / (difficulty_levels - 1)
    difficulty_map = {i + 1: i * difficulty_step + 0.1 for i in range(difficulty_levels)}
    selected_difficulty = st.slider("난이도 선택 (1-5단계)", min_value=1, max_value=difficulty_levels, value=3, step=1)
    difficulty = difficulty_map[selected_difficulty]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("새 게임"):
            st.session_state.board = create_sudoku_board(difficulty)
            st.session_state.original_board = st.session_state.board.copy()
            st.session_state.invalid_positions = []
            st.session_state.start_time = time.time()
    with col2:
        if st.button("난이도 적용"):
            st.session_state.board = create_sudoku_board(difficulty)
            st.session_state.original_board = st.session_state.board.copy()
            st.session_state.invalid_positions = []
            st.session_state.start_time = time.time()

    board = st.session_state.board
    original_board = st.session_state.original_board

    # 보드 표시
    colors = ["#FFEBEE", "#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#EDE7F6", "#FBE9E7", "#E1F5FE", "#F9FBE7"]

    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            box_id = (i // 3) * 3 + (j // 3)
            if original_board[i, j] != 0:
                cols[j].markdown(f'''
                    <div style="background-color: {colors[box_id]}; padding: 15px; text-align: center; 
                                font-size: 18px; font-weight: bold; border: 1px solid black;">
                        {original_board[i, j]}
                    </div>
                ''', unsafe_allow_html=True)
            else:
                input_value = cols[j].text_input(
                    f"cell_{i}_{j}",
                    value=str(board[i, j]) if board[i, j] != 0 else '',
                    max_chars=1,
                    label_visibility='collapsed',
                    key=f'input_{i}_{j}'
                )
                if input_value.isdigit() and 1 <= int(input_value) <= 9:
                    board[i, j] = int(input_value)
                else:
                    board[i, j] = 0

    if st.button("제출"):
        # 정답과 비교하여 틀린 개수 계산 (사용자 입력값만 체크)
        invalid_count = get_invalid_count(board, original_board)

        # 게임이 클리어된 경우
        if np.all(board != 0) and invalid_count == 0:
            elapsed_time = time.time() - st.session_state.start_time
            st.success(f"축하합니다! 스도쿠를 완성했습니다! 걸린 시간: {elapsed_time:.2f}초")

            # 점수 계산 로직
            final_score = calculate_score(selected_difficulty, elapsed_time)

            st.write(f"당신의 점수: {final_score}점")
            st.write(f"소요 시간: {elapsed_time:.2f}초")
            st.write(f"난이도: {selected_difficulty}단계")

            # 점수에 따른 추가 메시지
            if final_score >= 900:
                st.balloons()
                st.success("🏆 완벽한 성적! 스도쿠 마스터!")
            elif final_score >= 700:
                st.success("👏 훌륭합니다! 뛰어난 성적!")
            elif final_score >= 500:
                st.info("👍 좋은 성적입니다!")
            else:
                st.warning("🙌 더 나아질 수 있어요!")
        else:
            if np.all(board != 0):
                st.warning(f"📝 게임을 클리어하려면 모든 답을 정확히 입력해야 합니다. 틀린 답이 {invalid_count}개 있습니다.")
            else:
                st.warning("📝 아직 모든 칸을 채우지 않았습니다.")

    # 채팅창 추가
    with st.container(key="chat"):
        js_test.draw_chat()

if __name__ == "__main__":
    main()
