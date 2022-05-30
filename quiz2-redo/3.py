from queue import Queue
from time import sleep
from random import randint, randrange
from threading import Thread


class Tournament:
    def __init__(self, players: list):
        self.players = players
        self.stages = 0
        self._count_stages()

    def _count_stages(self):
        players = len(self.players)
        while players > 0:
            self.stages += 1
            players //= (2 + players % 2)
        self.stages += 1

    def start(self):
        # winner_queue = Queue()
        for stage in range(self.stages):
            print(f'------ STAGE {stage} --------')
            pairs = self._make_pairs()
            print(pairs)
            queues = [Queue() for _ in range(len(self.players) // 2)]
            for pair_num, (player1, player2) in enumerate(pairs):
                self._make_pair_play(player1, player2, queues[pair_num])
                winner = queues[pair_num].get()
                print(f'Player {winner.player_num} has won a battle')
                self.players.remove(winner)
        queue = Queue()
        self._make_pair_play(self.players[0], self.players[1], queue)
        print(f'Player {queue.get().player_num} has won a tournament')

    def _make_pair_play(self, player1, player2, queue):
        Thread(target=player1.play, args=(queue,)).start()
        Thread(target=player2.play, args=(queue,)).start()

    def _make_pairs(self):
        players = self.players[:]
        pairs = []
        while len(players) > 1:
            pairs.append((self._pop_random(players), self._pop_random(players)))
        return pairs

    def _pop_random(self, players: list):
        idx = randrange(0, len(players))
        return players.pop(idx)


class Player:
    def __init__(self, player_num: int):
        super().__init__()
        self.player_num = player_num

    def _toss(self):
        print(f"Player {self.player_num} is tossing...")
        sleep(randint(0, 3))
        return randint(1, 6)

    def play(self, queue: Queue):
        while True:
            result = self._toss()
            print(f"{self.player_num} got {result}")
            if result == 6:
                break
        queue.put(self)

    def __str__(self):
        return f'{self.player_num}'

    __repr__ = __str__


if __name__ == '__main__':
    players = [Player(i) for i in range(1, 11)]
    tour = Tournament(players)
    tour.start()
