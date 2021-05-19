def negamax(depth, alpha, beta):

        # Init PV length
        self.pv_length[self.ply] = self.ply

        # Depth = 0, return value from the quiescence search
        if depth == 0:
            return self.quiescence(alpha, beta)

        # Increment node count
        self.nodes += 1

        # Is own king in check?
        self.is_in_check = self.gamestate.is_square_attacked(self.gamestate.king_pos[self.gamestate.side_to_move], self.gamestate.side_to_move)

        # Check extension
        if self.is_in_check:
            depth += 1

        # Get pseudo legal moves
        children = mg.gen_moves(self.gamestate)

        # Sort the moves
        children = self.sort_moves(children)

        # If we are following PV line, we want to enable PV-scoring
        if self.follow_pv:
            self.enable_pv_scoring(children)

        # Init legal moves counter and best move so far
        self.legal_moves = 0

        # Number of moves searched in the moves list
        moves_searched = 0

        # Negamax recursive loop
        for child in children:

            # If move is legal, make it. Otherwise move on to the next candidate.
            if self.gamestate.make_move(child):

                # Increment legal moves and ply
                self.legal_moves += 1
                self.ply += 1

                # Do a normal search
                score = -self.negamax(depth - 1, -beta, -alpha)

                # Decrement ply and increase number of moves searched
                self.ply -= 1
                moves_searched += 1

                # Take back move
                self.gamestate.unmake_move()

                # Fail-hard beta cutoff (node fails high)
                if score >= beta:

                    # Store killer moves, only if it is a non-capturing move (used in move sorting)
                    if mg.extract_capture(child) == 0:
                        self.killer_moves[1][self.ply] = self.killer_moves[0][self.ply]
                        self.killer_moves[0][self.ply] = child

                    return beta

                # Found a better move (PV-node)
                if score > alpha:
                    alpha = score

                    # Store history moves, only if it is a non-capturing move (used in move sorting)
                    if mg.extract_capture(child) == 0:
                        self.history_moves[mg.extract_piece_moved(child)][mg.extract_to_square(child)] += depth

                    # Write PV move to PV table for the given ply
                    self.pv_table[self.ply][self.ply] = child

                    # Loop over the next ply
                    for next_ply in range(self.ply + 1, self.pv_length[self.ply + 1], 1):

                        # Copy move from deeper ply into current ply's line
                        self.pv_table[self.ply][next_ply] = self.pv_table[self.ply + 1][next_ply]

                    # Adjust PV length
                    self.pv_length[self.ply] = self.pv_length[self.ply + 1]

        # If we don't have a legal move to make in the position, check whether it's checkmate or stalemate
        if not self.legal_moves:

            # Checkmate, return checkmate score
            if self.is_in_check:
                return -1e9 + self.ply

            # Stalemate, return stalemate score
            return 0

        # Node fails low
        return alpha