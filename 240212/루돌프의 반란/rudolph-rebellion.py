def crash(ny,nx,dy,dx,santa_num,c,d):
    # ny,nx = 충돌당한 산타의 원래 위치, dy, dx = 산타 or 루돌프의 이동방향
    # santa_num = 충돌당한 산타 번호

    # 루돌프가 산타 박았을때
    if c :
        # 루돌프 이동뱡향으로 루돌프의 힘만큼 산타가 밀려나게됨.
        y, x = ny + dy*c, nx + dx*c

        # 범위 체크
        if 0 <= y < n and 0 <= x < n:
            # 산타는 기절해야하므로 현재턴과 다음턴까지 기절배열에 추가해줌.
            shock_santa[santa_num] += [turn, turn + 1]

            # 떨어진 위치가 산타인 경우
            if board[y][x] != 0:
                # 산타 위치 업데이트
                # 떨어진 산타를 보드에 넣고, 이동해야할 산타 넘버 업데이트 시켜주기
                surv_santa[santa_num] = (y, x)
                board[y][x], santa_num = santa_num, board[y][x]

                while True:
                    # 한칸씩 이동해야하므로 c 안곱함
                    y, x = y + dy, x + dx
                    # 범위 체크
                    if 0 <= y < n and 0 <= x < n:
                        # 산타일 경우 계속 반복 -> 산타의 연쇄적인 이동
                        if board[y][x] != 0:
                            surv_santa[santa_num] = (y, x)
                            board[y][x], santa_num = santa_num, board[y][x]
                        # 빈칸일 때
                        else:
                            surv_santa[santa_num] = (y, x)
                            board[y][x] = santa_num
                            break
                    # 다음 위치가 범위 밖일 경우 산타 제거
                    else:
                        surv_santa[santa_num] = False
                        break

            # 처음 날라간 산타가 떨어진 위치가 빈칸일때, 좌표 갱신 후 이동
            else:
                surv_santa[santa_num] = (y, x)
                board[y][x] = santa_num

        # 처음 날라간 산타가 떨어진 위치가 범위 밖일때, 산타 제거
        else:
            surv_santa[santa_num] = False

    # 산타가 루돌프 박았을 때
    elif d :
        # 산타 이동방향의 반대방향으로 산타의 힘만큼 밀려나게됨.
        y, x = ny - dy*d, nx - dx*d

        # 범위체크
        if 0 <= y < n and 0 <= x < n:
            # 기절
            shock_santa[santa_num] += [turn, turn + 1]

            # 처음 날아간 산타가 떨어진 곳에 산타가 있 경우
            if board[y][x] != 0:
                surv_santa[santa_num] = (y, x)
                board[y][x], santa_num = santa_num, board[y][x]

                while True:
                    y, x = y - dy, x - dx
                    if 0 <= y < n and 0 <= x < n:
                        # 산타일 경우 계속 반복 -> 산타의 연쇄적인 이동
                        if board[y][x] != 0:
                            surv_santa[santa_num] = (y, x)
                            board[y][x], santa_num = santa_num, board[y][x]
                        else:
                            surv_santa[santa_num] = (y, x)
                            board[y][x] = santa_num
                            break
                    # 다음 위치가 범위 밖일 경우 산타 제거
                    else:
                        surv_santa[santa_num] = False
                        break

            # 처음 날아간 산타가 떨어진 곳이 빈칸일 경우 산타 이동
            else:
                surv_santa[santa_num] = (y, x)
                board[y][x] = santa_num

        # 처음 날아간 산타가 떨어진 곳이 범위 밖일 경우 산타제거
        else:
            surv_santa[santa_num] = False

# 루돌프 이동 함수
def rudolf():
    global rr, rc       # 루돌프 좌표
    temp = [0] * p      # 루돌프와 산타의 거리를 계산한 뒤 r,c,거리 순으로 정렬해서 제일 조건에 적합한 산타 찾기 위한 배열

    # 처음 할일 = 제일 가까운 산타를 찾기
    for i in range(1,p+1):
        # 탈락한 산타라면 continue, 여기서 temp에 아무 튜플을 추가하는 이유는 105~107라인에서 정렬시 int가 들어가 있음 에러가 뜨기 때문.
        if not surv_santa[i]:
            temp[i-1] = (100000,100000,100000,i)
            continue

        # 생존 산타 좌표 받아와서 루돌프와 거리 계산 후 배열에 추가해놓기
        y,x = surv_santa[i]
        distance = (y-rr)**2 + (x-rc)**2
        temp[i-1] = (y,x,distance,i)

    # r좌표, c 좌표 큰순으로 정렬 후 거리 작은 순으로 정렬
    temp.sort(key=lambda x:(x[1]),reverse=True)
    temp.sort(key=lambda x:(x[0]),reverse=True)
    temp.sort(key=lambda x:x[2])

    # 제일 조건에 적합한 산타의 위치와 거리, 산타 번호 저장해놓기
    min_santa_y, min_santa_x, _, santa_num = temp[0]

    # 루돌프가 이동 후에 거리가 최소가 될때의 좌표, 그 거리를 저장하는 변수
    min_y, min_x, min_distance = 0,0,1000000000

    # 루돌프 8방향으로 이동하면서 픽한 산타와의 거리를 계산하면서 거리가 젤 최소가 되는 방향으로 이동하는 반복문
    # 이동 중에 산타를 만나면 산타를 밀쳐냄. 산타를 안만나면 자리만 이동
    for i in range(8):
        # 루돌프의 다음 위치와 그 위치에서의 산타와 거리 계산
        nrr, nrc = rr + rudolf_dir[i][0], rc + rudolf_dir[i][1]
        distance = (nrr-min_santa_y)**2 + (nrc-min_santa_x)**2

        # 만약 distance가 0이라면 이동한 자리에 산타가 있었단 얘기 == 충돌
        if distance == 0:
            # 그 위치에 루돌프 위치시킨 후 산타가 얻는 점수를 계산해주기
            board[rr][rc] = 0
            rr, rc = nrr, nrc
            board[rr][rc] = -1
            total_santa[santa_num] += c

            # 루돌프의 이동방향을 파악한 후, 충돌함수로 넘겨주기
            dy, dx = rudolf_dir[i]
            crash(rr,rc,dy,dx,santa_num,c,False)
            break

        # 가장 작아지는 방향으로 이동하기 위해 좌표 저장
        # 작아지는 방향이 여러개일 경우 가장 많이 작아지는 쪽으로 이동해야함.
        if distance < min_distance :
            min_distance = distance
            min_y, min_x = nrr, nrc
    else:
        # for문이 브레이크 안되고 여기까지 넘어오면 충돌 안한것
        # 그냥 루돌프 이동시켜주고 루돌프 좌표 갱신
        if 0 <= min_y < n and 0 <= min_x < n:
            board[rr][rc] = 0
            rr, rc = min_y, min_x
            board[rr][rc] = -1

# 산타 이동 함수
def santa():
    # 산타 차례대로 반복문
    for i in range(1,p+1):
        # 이 플래그는 산타가 이동을 할 수 있느냐 없느냐임.
        # 산타는 루돌프와 거리가 작아지는 쪽으로 이동해야함.
        # 1. 벽이나 산타에 가로막혀 이동을 하지 못하거나,
        # 2. 이동은 할 수 있지만 거리가 작아지지 않는 경우는 이동을 안해야함. 그거 체크하는 변수
        flag = False

        # 기절했거나, 죽은 산타는 패스
        if turn in shock_santa[i] or not surv_santa[i] :
            continue
        else:
            y, x = surv_santa[i]                              # 산타 좌표
            min_y, min_x, min_distance = 0,0,1000000000       # 루돌프와의 최소거리, 그때의 산타 위치를 저장하기 위한 변수
            before_distance = (y-rr)**2 + (x-rc)**2           # 이동전 산타-루돌프 거리를 저장해놓음.

            # 네 방향으로 돌아줌.
            for j in range(4):
                ny, nx = y + santa_dir[j][0], x + santa_dir[j][1]
                # 범위 안일때
                if 0<=ny<n and 0<=nx<n:
                    # 다음 위치가 빈칸일때
                    if board[ny][nx] == 0:
                        # 이동 후 거리를 측정해서 줄어들었을때만 이동가능함.
                        # 맞다면 이동 가능하니 flag 바꿔주고, 이동 가능한 것들중에
                        # 루돌프와의 거리를 최소로 만들어주는 위치로 이동하기 위해
                        # min_y, min_x, min_distance를 구해줌.
                        after_distance = (ny-rr)**2 + (nx-rc)**2
                        if after_distance < before_distance:
                            if after_distance < min_distance:
                                flag = True
                                min_distance = after_distance
                                min_y, min_x = ny, nx

                    # 다음 위치가 루돌프인 경우 = 충돌
                    # 원래 산타가 있던 위치 빈칸으로 만들어주고
                    # 산타 점수 처리해주고 산타이동방향을 충돌함수로 전달한다.
                    elif board[ny][nx] == -1:
                        board[y][x] = 0
                        dy, dx = santa_dir[j]
                        total_santa[i] += d
                        crash(ny,nx,dy,dx,i,False,d)
                        break

            # 산타가 네방향으로 이동했을때 루돌프와의 거리가 줄어드는 곳이 있을때 == 이동해야함
            # 아니면 이동안함.
            if flag :
                # 위에서 구한 최소거리, 그때의 인덱스로 산타이동, 산타 좌표 갱신
                board[y][x] = 0
                board[min_y][min_x] = i
                surv_santa[i] = (min_y,min_x)

if __name__=='__main__':
    n,m,p,c,d = map(int,input().split())                                    # n 맵크기, m 턴수, p 산타수, c-d 충돌시 점수
    board = [[0]*n for _ in range(n)]                                       # 맵
    total_santa = [0]*(p+1)                                                 # 전체산타배열
    surv_santa = [0]*(p+1)                                                  # 생존한 산타배열
    shock_santa = [[-1] for _ in range(p+1)]                                # 기절한 산타체크배열
    rudolf_dir = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]    # 루돌프 이동방향
    santa_dir = [(-1,0),(0,1),(1,0),(0,-1)]                                 # 산타 이동 방향

    # 루돌프 초기위치 루돌프는 -1로 표시
    rr, rc = map(int,input().split())
    rr, rc = rr-1, rc -1
    board[rr][rc] = -1

    # 산타수만큼 맵에 표시, 생존한 산타 번호에 맞게 위치 넣어주기
    for i in range(1,p+1):
        a, sr, sc = map(int,input().split())
        board[sr-1][sc-1] = a
        surv_santa[a] = (sr-1,sc-1)

    for turn in range(m):
        sflag = False
        # print('--------------%d턴---------------' % turn)

        # 루돌프 이동
        rudolf()
        # print('-----------루돌프이동-------------')
        # for i in range(n):
        #     for j in range(n):
        #         print('%3d'%board[i][j], end='')
        #     print()

        # 산타 이동
        santa()
        # print('-----------산타 이동-------------')
        # for i in range(n):
        #     for j in range(n):
        #         print('%3d'%board[i][j], end='')
        #     print()
        #
        # print()
        # 한턴 끝나면 생존한 산타들 점수 1씩 올려주기
        # 생존한 산타하나라도 있으면 sflag 변경
        for s in range(1,p+1):
            if surv_santa[s] :
                total_santa[s] += 1
                sflag = True

        if not sflag:
            break

    # 정답 출력
    for i in range(1,p+1):
        print(total_santa[i], end = ' ')