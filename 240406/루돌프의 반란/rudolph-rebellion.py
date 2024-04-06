from collections import deque
def move_rudolf():
    global ry, rx
    temp = []       # 산타 하나씩 검사하면서 조건에 가장 적합한 산타 얻기 / [산타번호,산타위치,둘사이거리]
    for i in range(1,p+1):
        sy, sx, shock, fail = santa[i]
        # 탈락안한 산타
        if fail == 0:
            dis = (sy-ry)**2 + (sx-rx)**2       # 거리 계산 후 후보에 추가
            temp.append([i,sy,sx,dis])

    temp.sort(key=lambda x:(x[3],-x[1],-x[2]))  # 가장가깝고, r,c 가장 큰 산타
    num, sy, sx, dis = temp[0]                  # 조건에 가장 적합한 산타

    min_val,min_y,min_x,rd = 100, 0, 0, 0
    for i in range(8):
        nry, nrx = ry + rudolf_dir[i][0], rx + rudolf_dir[i][1]
        n_dis = (nry-sy)**2 + (nrx-sx)**2       # 이동 후 거리 계산
        if n_dis < min_val:                     # 이동 후 거리 최소값 되는 곳 찾기
            min_val, min_y, min_x, rd = n_dis, nry, nrx, i

    board[ry][rx] = 0              # 루돌프 위치 갱신
    ry, rx = min_y, min_x
    if board[ry][rx] != 0:         # 루돌프 이동 위치에 산타가 있을때 산타는 루돌프 이동방향으로 c칸만큼 밀리게 됨.
        num = board[ry][rx]        # 튕겨난 산타 번호
        santa_score[num] += c      # 산타 점수 갱신
        board[ry][rx] = -9         # 루돌프 위치 갱신

        nsy, nsx = ry + rudolf_dir[rd][0]*c, rx + rudolf_dir[rd][1]*c   # 산타 튕겨난 위치 계산
        if 0<=nsy<n and 0<=nsx<n:                                       # 범위내일때
            if board[nsy][nsx] != 0:                                    # 다른 산타 있을때
                dq.append(board[nsy][nsx])                              # 다른 산타 추가

                board[nsy][nsx] = num                                   # 충돌 산타 업데이트
                santa[num] = [nsy,nsx,2,0]

                # 상호작용시작
                while dq:
                    num = dq.popleft()
                    sy, sx,_,_ = santa[num]
                    # 한칸이동
                    nsy, nsx = sy + rudolf_dir[rd][0], sx + rudolf_dir[rd][1]
                    if 0<=nsy<n and 0<=nsx<n:           # 범위내일때
                        if board[nsy][nsx] != 0:        # 다른 산타 있을때
                            dq.append(board[nsy][nsx])

                            board[nsy][nsx] = num
                            santa[num] = [nsy,nsx,0,0]
                        else:                           # 다른 산타 없을때
                            board[nsy][nsx] = num
                            santa[num] = [nsy, nsx, 0, 0]
                    else:                               # 범위 밖일때
                        santa[num] = [0,0,0,1]

            else:                                                       # 다른 산타 없을때
                board[nsy][nsx] = num
                santa[num] = [nsy,nsx,2,0]
        else:                                                           # 범위밖일때
            santa[num] = [0,0,0,1]
    else:
        board[ry][rx] = -9

def move_santa():
    # 산타 하나씩 꺼내면서 기절여부 탈락여부 검사
    for i in range(1,p+1):
        y, x, shock, fail = santa[i]
        ori_dis = (y-ry)**2 + (x-rx)**2
        if shock ==0 and fail == 0:
            min_val, min_y, min_x, sd  = ori_dis, -1, -1, 0
            # 우선순위 방향 돌며 거리가 줄어드는 쪽 구하기 (상 우 하 좌)
            for dd in range(4):
                sy, sx =  y + santa_dir[dd][0], x + santa_dir[dd][1]
                if 0<=sy<n and 0<=sx<n and board[sy][sx] <= 0:
                    dis = (ry - sy) ** 2 + (rx - sx) ** 2  # 루돌프와 거리 계산
                    if dis < min_val:
                        min_val,min_y,min_x,sd = dis,sy,sx,dd

            sy, sx = min_y, min_x
            if min_val == ori_dis:
                continue
            if (sy,sx) == (ry,rx):                # 루돌프 만났을때
                # 산타 -> 루돌프 충돌 구현
                santa_score[i] += d
                nsy = sy + d*santa_dir[(sd+2)%4][0]
                nsx = sx + d*santa_dir[(sd+2)%4][1]
                if 0 <= nsy < n and 0 <= nsx < n:  # 범위내일때
                    if board[nsy][nsx] != 0:  # 다른 산타 있을때
                        dq.append(board[nsy][nsx])  # 다른 산타 추가

                        board[y][x] = 0
                        board[nsy][nsx] = i  # 충돌 산타 업데이트
                        santa[i] = [nsy, nsx, 2, 0]

                        # 상호작용시작
                        while dq:
                            num = dq.popleft()
                            yy, xx, _, _ = santa[num]
                            # 한칸이동
                            nsy, nsx = yy + santa_dir[(sd+2)%4][0] , xx + santa_dir[(sd+2)%4][1]
                            if 0 <= nsy < n and 0 <= nsx < n:  # 범위내일때
                                if board[nsy][nsx] != 0:  # 다른 산타 있을때
                                    dq.append(board[nsy][nsx])

                                    board[nsy][nsx] = num
                                    santa[num] = [nsy, nsx, 0, 0]
                                else:  # 다른 산타 없을때
                                    board[nsy][nsx] = num
                                    santa[num] = [nsy, nsx, 0, 0]
                            else:  # 범위 밖일때
                                santa[num] = [0, 0, 0, 1]
                                board[yy][xx] = 0

                    else:  # 다른 산타 없을때
                        board[nsy][nsx] = i
                        board[y][x] = 0
                        santa[i] = [nsy, nsx, 2, 0]
                else:  # 범위밖일때
                    santa[i] = [0, 0, 0, 1]
                    board[y][x] = 0

            elif board[sy][sx] == 0:              # 빈칸일때
                board[y][x] = 0
                board[sy][sx] = i
                santa[i][0], santa[i][1] = sy,sx


if __name__=='__main__':
    n,m,p,c,d = map(int,input().split())        # n 맵크기 / m 게임턴수 / p 산타수 / c 루돌프 힘/ d 산타힘
    board = [[0]*n for _ in range(n)]           # 맵
    rudolf_dir = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    santa_dir = [(-1,0),(0,1),(1,0),(0,-1)]
    dq =  deque()                               # 상호작용 큐
    santa_score = [0]*(p+1)                     # 산타 점수배열

    ry, rx = map(int,input().split())           # 루돌프 초기 위치
    ry, rx = ry - 1, rx - 1
    board[ry][rx] = -9                          # 맵에 표기

    # 산타 정보 저장
    santa = [0]*(p+1)           # 인덱스 = 산타번호 / [행,열,기절여부,탈락여부]
    for _ in range(p):
        num, y, x = map(int,input().split())        # 산타 번호와 위치
        santa[num] = [y-1,x-1,0,0]
        board[y-1][x-1] = num                       # 맵에 표기

    # m개의 턴 진행
    for turn in range(m):
        # [1] 루돌프 이동
        move_rudolf()
        # [2] 산타 이동
        move_santa()
        # [3] 산타 전원 탈락 여부 검사
        for i in range(1,p+1):
            if santa[i][3] == 0:
                break
        else:
            break

        # [4] 탈락안한 산타들 점수 1점씩 부여 / 기절한 산타 -1 씩해주기
        for i in range(1,p+1):
            if santa[i][3] == 0:
                santa_score[i] += 1
            if santa[i][2] > 0 :
                santa[i][2] -= 1

    for i in range(1,p+1):
        print(santa_score[i],end = ' ')