import streamlit as st
import numpy as np
import time
import random

# Set page configuration
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# Minimal CSS that works with both light and dark mode
st.markdown("""
<style>
    .centered-text {
        text-align: center;
    }
    .game-board {
        max-width: 300px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), "")
if 'current_player' not in st.session_state:
    st.session_state.current_player = "X"
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'ai_score' not in st.session_state:
    st.session_state.ai_score = 0
if 'draw_score' not in st.session_state:
    st.session_state.draw_score = 0
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "ai"  # Default to AI mode
if 'ai_difficulty' not in st.session_state:
    st.session_state.ai_difficulty = "medium"  # Default to medium difficulty
if 'loading' not in st.session_state:
    st.session_state.loading = False

# Display title and subtitle
st.markdown("<h1 style='text-align: center;'>Tic Tac Toe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Play against AI or a friend</p>", unsafe_allow_html=True)

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

# AI function with proper difficulty levels
def get_ai_move(board, difficulty):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i, j] == ""]
    
    if not empty_cells:
        return None
    
    # Easy: Just make random moves
    if difficulty == "easy":
        return random.choice(empty_cells)
    
    # Medium and Hard: Check if AI can win in the next move
    for i, j in empty_cells:
        board[i, j] = "O"
        if check_winner(board, "O"):
            board[i, j] = ""
            return (i, j)
        board[i, j] = ""
    
    # Medium and Hard: Check if player can win in the next move and block
    for i, j in empty_cells:
        board[i, j] = "X"
        if check_winner(board, "X"):
            board[i, j] = ""
            return (i, j)
        board[i, j] = ""
    
    # Medium: Take center if available, otherwise random
    if difficulty == "medium":
        if board[1, 1] == "":
            return (1, 1)
        else:
            return random.choice(empty_cells)
    
    # Hard: More strategic play
    if difficulty == "hard":
        # Take center if available
        if board[1, 1] == "":
            return (1, 1)
        
        # Look for fork opportunities (where AI can create two winning paths)
        # This is a simplified version of fork detection
        if board[1, 1] == "O":
            # If center is O, look for specific patterns
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            corner_count = sum(1 for i, j in corners if board[i, j] == "O")
            
            if corner_count == 1:
                # If one corner is O, try to take the opposite corner
                for i, j in corners:
                    if board[i, j] == "O":
                        opposite_i, opposite_j = 2-i, 2-j
                        if board[opposite_i, opposite_j] == "":
                            return (opposite_i, opposite_j)
        
        # Take corners if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if board[corner[0], corner[1]] == ""]
        if available_corners:
            return random.choice(available_corners)
        
        # Take edges if available
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_edges = [edge for edge in edges if board[edge[0], edge[1]] == ""]
        if available_edges:
            return random.choice(available_edges)
    
    # Fallback to random move
    return random.choice(empty_cells)

# Function to make a player move
def make_move(row, col):
    # If the game is over or the cell is already occupied, do nothing
    if st.session_state.game_over or st.session_state.board[row, col] != "":
        return
    
    # Set loading state
    st.session_state.loading = True
    
    # Make the move
    st.session_state.board[row, col] = st.session_state.current_player
    
    # Check if the current player has won
    if check_winner(st.session_state.board, st.session_state.current_player):
        st.session_state.game_over = True
        st.session_state.winner = st.session_state.current_player
        
        # Update scores
        if st.session_state.winner == "X":
            st.session_state.player_score += 1
        else:
            st.session_state.ai_score += 1
            
    # Check if it's a draw
    elif is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        st.session_state.draw_score += 1
    # Switch to the other player
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
        
        # If it's AI's turn in AI mode, make the AI move
        if st.session_state.game_mode == "ai" and st.session_state.current_player == "O" and not st.session_state.game_over:
            # Add a small delay to make it feel more natural
            time.sleep(0.5)
            
            # Get the AI move
            ai_move = get_ai_move(st.session_state.board, st.session_state.ai_difficulty)
            
            if ai_move:
                ai_row, ai_col = ai_move
                
                # Make the AI move
                st.session_state.board[ai_row, ai_col] = "O"
                
                # Check if AI has won
                if check_winner(st.session_state.board, "O"):
                    st.session_state.game_over = True
                    st.session_state.winner = "O"
                    st.session_state.ai_score += 1
                # Check if it's a draw after AI's move
                elif is_board_full(st.session_state.board):
                    st.session_state.game_over = True
                    st.session_state.winner = "Draw"
                    st.session_state.draw_score += 1
                else:
                    # Switch back to player X
                    st.session_state.current_player = "X"
    
    # Reset loading state
    st.session_state.loading = False

# Function to reset the game
def reset_game():
    st.session_state.board = np.full((3, 3), "")
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.loading = False
    
# Function to set game mode
def set_game_mode(mode):
    st.session_state.game_mode = mode
    reset_game()

# Function to set AI difficulty
def set_ai_difficulty(difficulty):
    st.session_state.ai_difficulty = difficulty
    reset_game()

# Game Controls Section
col1, col2 = st.columns(2)

with col1:
    # Game mode selector
    st.markdown("### Game Mode")
    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        if st.button("Human vs AI", 
                     type="primary" if st.session_state.game_mode == "ai" else "secondary",
                     use_container_width=True):
            set_game_mode("ai")
    
    with mode_col2:
        if st.button("Human vs Human", 
                     type="primary" if st.session_state.game_mode == "human" else "secondary",
                     use_container_width=True):
            set_game_mode("human")

with col2:
    # Show difficulty selector only in AI mode
    if st.session_state.game_mode == "ai":
        st.markdown("### AI Difficulty")
        diff_col1, diff_col2, diff_col3 = st.columns(3)
        
        with diff_col1:
            if st.button("Easy", 
                         type="primary" if st.session_state.ai_difficulty == "easy" else "secondary",
                         use_container_width=True):
                set_ai_difficulty("easy")
        
        with diff_col2:
            if st.button("Medium", 
                         type="primary" if st.session_state.ai_difficulty == "medium" else "secondary",
                         use_container_width=True):
                set_ai_difficulty("medium")
        
        with diff_col3:
            if st.button("Hard", 
                         type="primary" if st.session_state.ai_difficulty == "hard" else "secondary",
                         use_container_width=True):
                set_ai_difficulty("hard")

# Score Board
st.markdown("### Score")
score_cols = st.columns(3)

with score_cols[0]:
    st.metric(label="You (X)" if st.session_state.game_mode == "ai" else "Player X", 
              value=st.session_state.player_score)

with score_cols[1]:
    st.metric(label="Draws", value=st.session_state.draw_score)

with score_cols[2]:
    st.metric(label="AI (O)" if st.session_state.game_mode == "ai" else "Player O", 
              value=st.session_state.ai_score)

# Display loading spinner if loading
if st.session_state.loading:
    st.spinner("Thinking...")

# Display game status
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.success("Game Over: It's a Draw! 🤝")
    elif st.session_state.winner == "X":
        st.success("You Win! 🎉" if st.session_state.game_mode == "ai" else "Player X Wins! 🎉")
    else:
        st.error("AI Wins! 🤖" if st.session_state.game_mode == "ai" else "Player O Wins! 🎉")
else:
    current_player_name = (
        "Your Turn (X)" if st.session_state.current_player == "X" and st.session_state.game_mode == "ai" 
        else "AI's Turn (O)" if st.session_state.current_player == "O" and st.session_state.game_mode == "ai"
        else f"Player {st.session_state.current_player}'s Turn"
    )
    
    st.info(current_player_name)

# Create the game board
st.markdown('<div class="game-board">', unsafe_allow_html=True)
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        with cols[col]:
            # Get the current cell value
            cell_value = st.session_state.board[row, col]
            
            # Button styling based on cell value
            button_label = cell_value if cell_value else " "
            
            # Determine button style based on cell value
            if cell_value == "X":
                button_style = "primary"
            elif cell_value == "O":
                button_style = "secondary"  # Changed from "error" to "secondary"
            else:
                button_style = "secondary"
            
            # Use a unique key for each button
            button_key = f"cell_{row}_{col}"
            
            # Create the button
            if st.button(button_label, key=button_key, type=button_style, disabled=st.session_state.game_over or st.session_state.loading):
                make_move(row, col)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Game controls
if st.button("New Game", type="primary", use_container_width=True, disabled=st.session_state.loading):
    reset_game()
    st.rerun()