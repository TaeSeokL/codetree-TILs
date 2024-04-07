def crash(num,y,x,dy,dx,mul):
    dq = [(num,y,x,dy,dx,mul)]

    while dq:
        # 충돌한 산타 정보
        num,y,x,dy,dx,mul = dq.pop(0)

        # 산타 착지 위치 계산
        ny = y + dy*mul
        nx = x + dx*mul

        # 범위내일때
        if 0<=ny<n and 0<=nx<n:
            # 착지위치가 빈칸일때
            if board[ny][nx] == 0:
                board[ny][nx] = num     # 산타 맵에 표시
                santa[num] = [ny,nx]    # 산타 위치 갱신
                return
            # 착지위치에 산타있을때
            else:
                dq.append((board[ny][nx],ny,nx,dy,dx,1))        # 연쇄작용을 위해 그 산타도 큐에 추가해준다.
                board[ny][nx] = num
                santa[num] = [ny,nx]
        # 범위밖일때 -> 탈락
        else:
            santa_alive[num] = 0
            return


if __name__=='__main__':
    n,m,p,c,d = map(int,input().split())        # n 맵크기 / m 게임턴수 / p 산타수 / c 루돌프 힘/ d 산타힘
    board = [[0]*n for _ in range(n)]           # 맵
    rudolf_dir = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    santa_dir = [(-1,0),(0,1),(1,0),(0,-1)]

    ry, rx = map(int,input().split())           # 루돌프 초기 위치
    ry, rx = ry - 1, rx - 1
    board[ry][rx] = -1                          # 맵에 표기

    # 산타 정보 저장
    santa = [0]*(p+1)                               # 산타 위치 배열 [행,열] / 인덱스 = 산타번호
    for _ in range(p):
        num, y, x = map(int,input().split())        # 산타 번호와 위치
        santa[num] = [y-1,x-1]
        board[y-1][x-1] = num                       # 맵에 표기

    santa_shock = [0] * (p + 1)  # 산타 기절 여부
    santa_alive = [1] * (p + 1)  # 산타 탈락 여부
    santa_score = [0] * (p + 1)  # 산타 점수 배열

    # m개의 턴 진행
    for turn in range(m):
        # [1] 루돌프 이동
        # [1-1] 현재 루돌프 위치에서 가장 가까운 산타 찾기
        temp_lst = []
        for num in range(1,p+1):
            if santa_alive[num] == 1:                       # 산타가 탈락 안했을때만 진행
                sy,sx = santa[num]
                dis = (ry-sy)**2 + (rx-sx)**2

                temp_lst.append((num,sy,sx,dis))            # 산타번호,행,열,거리 순으로 저장해두기

        temp_lst.sort(key=lambda x:(x[3],-x[1],-x[2]))  # 산타들 중 거리가 가깝고, 행과 열이 큰 놈 찾기
        snum,sy,sx,dis = temp_lst[0]                    # 가장 적합한 산타 찾음.

        # [1-2] 루돌프 인접 8방향 중 위에서 찾은 산타와 가장 가까워지는 위치 구하기
        min_dis = dis           # 원래 산타와의 거리보다 가까워져야하므로 이렇게 초기화
        min_y,min_x = -1,-1     # 가장 가까워지는 방향으로 이동시 위치 저장 변수
        dy, dx = -2,-2          # 가장 가까워지는 방향으로 이동시 이동 방향
        for rdy, rdx in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1,),(0,-1),(-1,-1)):
            nry = ry + rdy
            nrx = rx + rdx

            n_dis = (nry-sy)**2 + (nrx-sx)**2       # 이동 후 산타와의 거리 구하기
            if n_dis<min_dis:                       # 만약 거리가 줄어든다면 업데이트
                min_dis = n_dis
                min_y, min_x = nry, nrx
                dy,dx = rdy,rdx

        # 루돌프 이동 위치 구했으면 예전 위치 지워주고 위치 업데이트
        board[ry][rx] = 0
        ry, rx = min_y,min_x

        if board[ry][rx] != 0:          # 이동 위치에 산타가 있을때 : 충돌!
            num = board[ry][rx]         # 충돌한 산타 번호
            santa_score[num] += c       # 산타 점수 주기
            santa_shock[num] = 2        # 산타 기절 처리
            board[ry][rx] = -1          # 루돌프 맵에 표시
            crash(num,ry,rx,dy,dx,c)    # 충돌한 산타 충돌함수로 전달

        else:                           # 이동 위치 빈칸일때 : 루돌프 맵에 표시
            board[ry][rx] = -1

        # [2] 산타 이동 : 산타 하나씩 꺼내서 루돌프와 가까워지는 곳 계산
        for num in range(1,p+1):
            # 기절상태거나, 탈락 산타는 스킵
            if santa_shock[num]>0 or santa_alive[num] == 0 :    continue

            sy, sx = santa[num]
            dis = (ry-sy)**2 + (rx-sx)**2       # 현재 산타 위치에서 루돌프와 거리 계산
            min_dis = dis
            min_y,min_x = -1,-1
            dy, dx = -2, -2
            for sdy, sdx in ((-1,0),(0,1),(1,0),(0,-1)):            # 상우하좌 탐색
                nsy, nsx = sy + sdy, sx + sdx
                if 0<=nsy<n and 0<=nsx<n and board[nsy][nsx] <= 0:  # 범위내이고 산타가 없는 곳으로만 이동
                    n_dis = (ry-nsy)**2 + (rx-nsx)**2
                    if min_dis > n_dis:
                        min_dis = n_dis                             # 최대로 가까워지는 거리
                        min_y, min_x = nsy,nsx                      # 그때 산타 위치
                        dy, dx = sdy,sdx                            # 그때 이동 방향

            if min_dis == dis:          continue            # 거리가 가까워지는 곳이 없으면 스킵

            board[sy][sx] = 0           # 산타 위치 지워주기
            santa[num] = [min_y,min_x]  # 산타 위치 갱신

            if (min_y,min_x) == (ry,rx):            # 루돌프와 충돌한 경우
                santa_score[num] += d               # 산타 점수 누적
                santa_shock[num] = 2                # 산타기절 처리
                crash(num,min_y,min_x,-dy,-dx,d)    # 충돌함수 전달
            else:                           # 빈칸일 경우
                board[min_y][min_x] = num

        # [3] 산타 전원 탈락 여부 검사
        if santa_alive.count(0) == p:
            break

        # [4] 탈락안한 산타들 점수 1점씩 부여 / 기절한 산타 -1 씩해주기
        for i in range(1,p+1):
            if santa_alive[i] == 1:
                santa_score[i] += 1
            if santa_shock[i] > 0:
                santa_shock[i] -= 1

    for i in range(1,p+1):
        print(santa_score[i],end = ' ')