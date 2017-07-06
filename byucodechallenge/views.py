from django.shortcuts import render
from .models import ChessBoard
import sys, requests, json

def chess_board(request):
    # new chess board layout
    Board = ChessBoard()
    # show layout if 'fen' was posted
    if request.POST.get('fen'):
        Board.fen = request.POST.get('fen')
        # perform a recommended chess move if 'move' was posted
        if (request.POST.get('move') == 'true'):
            try:
                # get recommended move
                api_response = requests.get('https://syzygy-tables.info/api/v2?fen=' + Board.fen)
            except requests.exceptions.RequestException as e:
                # our api request failed
                Board.api_error = e
            try:
                # convert to api response to json and get the first option in 'moves'
                moves = json.loads(api_response.text)['moves']
                recommended_move = next(iter(moves))
                # move chess pieces
                Board.move(recommended_move)
            except:
                # the api didn't return a move, probably because the FEN is invalid
                Board.moved = 'no recommended move from API'
    # pass the chess board to the view template
    return render(request, 'byucodechallenge/chess.html', {'board': Board})
 