def move_player():
    for num in range(len(player)):
        y,x,d = player[num]
        dis = abs(sy-y) + abs(sx-x)         # 술래와 거리가 3이하인 애들만 이동
        if dis <= 3:
            ny = y + dir[d][0]
            nx = x + dir[d][1]

            # 범위밖일때 -> 방향 정반대
            if ny < 0 or ny >= n or nx <0 or nx >= n:
                # 방향 업데이트
                d = (d+2)%4
                player[num][2] = d
                # 다음 위치 다시 구하기
                ny = y + dir[d][0]
                nx = x + dir[d][1]

            # 이동 위치가 술래가 아닐때 -> 이동
            if (ny,nx) != (sy,sx):
                player[num] = [ny,nx,d]
                # 디버깅용
                board[y][x].pop()
                board[ny][nx].append(1)

if __name__=='__main__':
    n,m,h,k = map(int,input().split())                      # n 격자크기 / m 도망자수 / h 나무수 / k 라운드수
    board = [[[] for _ in range(n)] for _ in range(n)]      # 맵생성(디버깅용)

    # 플레이어 정보 저장
    player = []
    for _ in range(m):
        y,x,d = map(int,input().split())        # 도망자 초기 위치와 방향
        player.append([y-1,x-1,d])              # d == 1이면 좌우방향 도망자 / d == 2이면 상하방향 도망자
        board[y-1][x-1].append(1)               # 디버깅용 맵표시

    # 나무 정보 저장
    tree = []
    for _ in range(h):
        y,x = map(int,input().split())
        tree.append((y-1,x-1))

    dir = [(-1,0),(0,1),(1,0),(0,-1)]   #(상우하좌)
    ans = 0

    # 토네이도 변수들 초기화
    sy = sx = n // 2
    cnt, max_cnt, flag, val, sd = 0, 1, 0, 1, 0

    # 턴수만큼 게임 진행
    for turn in range(1,k+1):
        # [1] 도망자 이동
        move_player()

        # [2] 술래이동
        cnt += 1
        sy = sy + dir[sd][0]
        sx = sx + dir[sd][1]

        if (sy,sx) == (0,0):        cnt, max_cnt, flag, val ,sd  = 1, n-1, 1, -1, 2     # (0,0)에 왔을때 안쪽 토네이도 위한 초기화
        if (sy,sx) == (n//2,n//2):  cnt, max_cnt, flag, val ,sd  = 0, 1, 0, 1, 0        # 정가운데 왔을때 바깥쪽 토네이도 위한 초기화

        if cnt == max_cnt:
            cnt = 0
            sd = (sd+val)%4
            if flag == 1:
                max_cnt += val
                flag= 0
            else:
                flag = 1

        # [3] 술래잡기
        sula_area = [(sy,sx)]          # 술래가 감시 가능한 영역
        ny, nx = sy,sx
        for _ in range(2):
            ny = ny + dir[sd][0]
            nx = nx + dir[sd][1]

            if 0<=ny<n and 0<=nx<n:    # 술래칸 포함 3칸 범위내이면 감시영역에 추가
                sula_area.append((ny,nx))

        # [4] 도망자들 잡기 -> 밑에서부터 돌면서 잡히면 pop
        for num in range(len(player)-1,-1,-1):
            y, x, _ = player[num]
            # 술래 감시 영역에 있는데, 나무가 없을때 = 잡힘
            if (y,x) in sula_area and (y,x) not in tree:
                player.pop(num)     # 도망자 제거
                ans += turn         # 점수누적
                board[y][x].pop()   # 디버깅용

    print(ans)