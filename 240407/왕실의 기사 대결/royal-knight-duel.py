from collections import deque

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
        if energy[num] > 0 :     # 기사가 살아있을때
            flag = 1
            after_move = [[] for _ in range(N+1)]      # 기사들 이동 후 위치 저장 (번호,행,열)
            damage_player = []   # 데미지 받을 기사 번호들
            dq = deque()         # 탐색큐
            # 명령받은 기사 탐색큐에 추가
            for pos in player[num]:
                y,x = pos
                dq.append((num,y,x))

            # 큐 빌때까지 탐색
            while dq:
                n,y,x = dq.popleft()

                ny = y + dir[d][0]
                nx = x + dir[d][1]
                # 이동 후 위치가 범위 내일때
                if 0<=ny<L and 0<=nx<L :
                    # 이동 후 칸이 벽일때 -> 밀린칸 배열 초기화 후 종료
                    if board[ny][nx] == 2:
                        flag = 0
                        continue
                    # 벽이 아니면 다 갈 수 있음.
                    else:
                        # 밀린칸 배열에 추가
                        after_move[n].append([ny,nx])

                        # 이동 후 칸에 다른 기사가 있을때
                        if player_board[ny][nx] > 0 and player_board[ny][nx] != n:
                            addi_num = player_board[ny][nx]
                            if addi_num not in damage_player:   # 중복방지
                                damage_player.append(addi_num)
                                for pos in player[addi_num]:
                                    y, x = pos
                                    dq.append((addi_num, y, x))
                # 이동 후 위치가 범위 밖일때
                else:
                    flag = 0
                    continue

            # 밀린 칸 배열이 존재할때
            if flag == 1:
                # 움직여야하는 기사들 위치 지우고 위치 갱신
                for num in range(1,N+1):
                    if after_move[num]:
                        # 원래 위치 지워주기
                        for y,x in player[num]:
                            player_board[y][x] = 0

                        player[num] = after_move[num]   # 위치갱신

                for num in range(1,N+1):
                    for y, x in player[num]:
                        player_board[y][x] = num    # 밀린 위치 업데이트

                # 데미지 받아야하는 기사들 꺼내서 데미지 입혀주기
                for num in damage_player:
                    for y,x in player[num]:
                        if (y,x) in trap and energy[num] > 0:
                            energy[num] -= 1

                            # 기사 체력이 다 까졌을떄 -> 맵에서 지워주기
                            if energy[num] == 0:
                                for y,x, in player[num]:
                                    player_board[y][x] = 0

    # 정답 계산
    ans = 0
    for num in range(1,N+1):
        if energy[num] > 0 :
            ans += ori_energy[num] - energy[num]

    print(ans)