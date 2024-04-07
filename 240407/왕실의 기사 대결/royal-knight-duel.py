from collections import deque

def horse_move(num, d):
    maybe_horses = deque()  # 움직일 가능성이 있는 기사번호 저장
    moving_horses = []      # 최종적으로 움직여야하는 기사번호 저장

    maybe_horses.append(num)

    while maybe_horses:
        n = maybe_horses.popleft()  # 움직일 가능성있는 기사 기준 명령 방향으로 탐색

        for y, x in player[n]:
            ny = y + dir[d][0]
            nx = x + dir[d][1]

            # 범위내이고
            if 0 <= ny < L and 0 <= nx < L:
                # 벽이면 못움직임
                if board[ny][nx] == 2:
                    return

                else:
                    # 범위내이고 벽아니면 일단 이동가능 -> 중복제거
                    if n not in moving_horses:
                        moving_horses.append(n)

                    # 다른 기사 있을 경우 또 탐색 해줌.
                    if player_board[ny][nx] != n and player_board[ny][nx] != 0:
                        if player_board[ny][nx] not in maybe_horses:
                            maybe_horses.append(player_board[ny][nx])
            # 범위밖이면 못움직임
            else:
                return

    # ---여기까지 도착한거면 moving_horses에 있는 애들은 다 움직일 수 있는거임.
    # 데미지 입힐애들을 먼저 구해야하기 때문에 moving_horses 카피해주고 명령받은애는 빼줌.
    damage_player = moving_horses[:]
    damage_player.remove(num)

    # 기사들 위치를 업데이트해주고, 원래 있던 자리에서 없애줌.
    for n in moving_horses:
        temp = []
        for y, x in player[n]:
            ny, nx = y + dir[d][0], x + dir[d][1]

            temp.append([ny, nx])
            player_board[y][x] = 0
        player[n] = temp

    # 기사들 새로운 위치에 넣어줌.
    for n in moving_horses:
        for y, x in player[n]:
            player_board[y][x] = n
    # for n in range(1,N+1):
    #     for y,x in player[n]:
    #         player_board[y][x] = n

    # 기사들 데미지 입혀줌.
    for n in damage_player:
        for y, x in player[n]:
            if (y, x) in trap and energy[n] > 0:
                energy[n] -= 1

                if energy[n] == 0:
                    for y, x, in player[num]:
                        player_board[y][x] = 0

if __name__=='__main__':
    L, N, Q = map(int,input().split())              # L 격자크기 / N 기사수 / Q 명령수

    board = [list(map(int,input().split())) for _ in range(L)]  # 빈칸0, 함정1, 벽 정보2
    player_board = [[0]*L for _ in range(L)]        # 기사 배열
    dir = [(-1,0),(0,1),(1,0),(0,-1)]               # 방향 (상 우 하 좌)

    # 함정 위치
    trap = []
    for r in range(L):
        for c in range(L):
            if board[r][c] == 1:
                trap.append((r,c))

    player = [[] for _ in range(N+1)]               # 기사별 위치 정보 / 인덱스 = 기사번호
    energy = [0]*(N+1)                              # 기사별 체력 정보

    for i in range(1,N+1):
        r,c,h,w,k = map(int,input().split())        # (r,c) 위치 / (h,w) 방패크기 / k 체력
        r, c = r-1 ,c-1
        energy[i] = k                               # 체력저장

        for y in range(r,r+h):
            for x in range(c,c+w):
                player[i].append([y,x])             # 기사가 차지하는 위치 전부 저장해두기
                player_board[y][x] = i              # 기사 맵에 표시

    ori_energy = energy[:]                          # 처음 체력 저장해두기

    for turn in range(Q):
        num, d = map(int,input().split())           # 명령받은 기사와 방향

        # 기사 죽은 경우 스킵
        if energy[num] == 0 :    continue

        horse_move(num,d)

    # 정답 계산
    ans = 0
    for num in range(1,N+1):
        if energy[num] > 0 :
            ans += ori_energy[num] - energy[num]

    print(ans)