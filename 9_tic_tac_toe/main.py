import streamlit as st
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# Add title and description
st.title("Tic Tac Toe")
st.markdown("A classic two-player game built with Streamlit")

# Initialize the game state in session state if not already present
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), "")
if 'current_player' not in st.session_state:
    st.session_state.current_player = "X"
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

# Function to check if a player has won
def check_winner(board, player):
    # Check rows
    for row in range(3):
        if all(board[row, col] == player for col in range(3)):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row, col] == player for row in range(3)):
            return True
    
    # Check diagonals
    if all(board[i, i] == player for i in range(3)) or all(board[i, 2-i] == player for i in range(3)):
        return True
    
    return False

# Function to check if the board is full (draw)
def is_board_full(board):
    return all(cell != "" for cell in board.flatten())

# Function to handle a move
def make_move(row, col):
    # If the game is over or the cell is already occupied, do nothing
    if st.session_state.game_over or st.session_state.board[row, col] != "":
        return
    
    # Make the move
    st.session_state.board[row, col] = st.session_state.current_player
    
    # Check if the current player has won
    if check_winner(st.session_state.board, st.session_state.current_player):
        st.session_state.game_over = True
        st.session_state.winner = st.session_state.current_player
    # Check if it's a draw
    elif is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
    # Switch to the other player
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# Function to reset the game
def reset_game():
    st.session_state.board = np.full((3, 3), "")
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None

# Display game status
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.subheader("Game Over: It's a Draw!")
    else:
        st.subheader(f"Game Over: Player {st.session_state.winner} wins! 🎉")
else:
    st.subheader(f"Current Player: {st.session_state.current_player}")

# Create the game board using a grid of buttons
st.write("---")
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        with cols[col]:
            # Get the current cell value
            cell_value = st.session_state.board[row, col]
            
            # Create a button with appropriate styling
            button_label = cell_value if cell_value else " "
            button_color = "primary" if cell_value == "X" else "secondary" if cell_value == "O" else "light"
            
            # Use a unique key for each button
            button_key = f"cell_{row}_{col}"
            
            # Create the button with custom CSS to make it square and larger
            st.markdown(
                f"""
                <style>
                div[data-testid="stButton"] > button {{
                    width: 80px;
                    height: 80px;
                    font-size: 32px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 5px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            
            if st.button(button_label, key=button_key):
                make_move(row, col)
                st.rerun()

st.write("---")

# Reset button
if st.button("New Game", type="primary"):
    reset_game()
    st.rerun()

# Add instructions
with st.expander("How to Play"):
    st.write("""
    1. Players take turns placing X or O on the board.
    2. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins.
    3. If all cells are filled and no player has won, the game is a draw.
    4. Click 'New Game' to start over.
    """)