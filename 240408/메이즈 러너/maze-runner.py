def move_player():
    global ans
    # 참가자 한명씩 꺼내서 출구좌표와 가까워지는 곳으로 이동한다.
    for i in range(len(player)-1,-1,-1):
        y,x = player[i]
        dis = abs(ey-y) + abs(ex-x)         # 참가자와 출구의 현재 최단거리
        min_dis, min_y,min_x = dis, -1, -1  # 최단거리 구하기 위한 변수

        for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):
            ny, nx = y + dy, x + dx

            if 0<=ny<n and 0<=nx<n :        # 범위내
                if (ny,nx) == (ey,ex):    # 이동한 곳이 출구라면 정답 누적 후 바로 탈출
                    ans += 1
                    player.pop(i)
                    break
                elif board[ny][nx] == 0:      # 빈칸일경우
                    n_dis = abs(ey-ny) + abs(ex-nx)     # 이동 후 출구와 거리 계싼
                    if n_dis < min_dis:
                        min_dis, min_y, min_x = n_dis,ny,nx


        # 상하좌우 움직여도 거리 안줄어들면 안움직임
        if min_dis == dis :     continue

        player[i] = [min_y,min_x]   # 참가자 이동
        ans += 1

def find_square():
    for l in range(2, n):  # l = 정사각형 크기 / 2부터 n-1까지 가질 수 있음.
        for r in range(n):
            for c in range(n):
                    if (r + l) > n or (c + l) > n:    continue

                    # 참가자 한명씩 보면서 정사각형 안에 포함되는지 확인
                    for y, x in player:
                        if r <= y < (r + l) and c <= x < (c + l) and r <= ey < (r + l) and c <= ex < (c + l):
                            return (r,c,l)

def rotate(r,c,l):
    global ey,ex
    # [1] 미로 회전 처리
    # [1-1]내구도 깎아주기
    for y in range(l):
        for x in range(l):
            if board[y+r][x+c] > 0:
                board[y+r][x+c] -= 1

    # [1-2] 미로 회전 처리 해주기
    for y in range(l):
        for x in range(l):
            next_board[y+r][x+c] = board[l-1-x+r][y+c]

    # [1-3] 원래 보드로 옮겨주기
    for y in range(l):
        for x in range(l):
            board[y+r][x+c] = next_board[y+r][x+c]

    # [2] 참가자 회전 처리
    for i in range(len(player)):
        y,x = player[i]

        # 참가자가 정사각형 안에 포함되는 경우
        if r<=y<r+l and c<=x<c+l:
            # 원점으로 바꾸기
            y,x = y-r, x - c
            # 회전 좌표 구하기
            new_y = x
            new_x = l-y-1
            # r,c 더하기
            new_y += r
            new_x += c

            player[i] = [new_y,new_x]

    # [3] 출구 회전 처리
    ey = ey - r
    ex = ex - c

    new_ey = ex
    new_ex = l - ey - 1

    new_ey += r
    new_ex += c
    ey, ex = new_ey, new_ex

if __name__=='__main__':
    n, m, k = map(int,input().split())                          # n 맵크기 / m 참가자수 / k 게임시간

    board = [list(map(int,input().split())) for _ in range(n)]  # 맵정보
    next_board = [[0]*n for _ in range(n)]                      # 임시저장배열
    player = []                         # 참가자 위치 관리 배열 [행,열]
    for _ in range(m):
        r,c = map(int,input().split())  # 참가자 초기 위치
        player.append([r-1,c-1])

    ey, ex = map(int,input().split())   # 출구 초기 위치
    ey, ex = ey - 1, ex - 1

    ans = 0     # 정답변수(참가자이동거리합)

    for turn in range(k):
        # [1] 참가자 이동
        move_player()
        # [2] 참가자 모두 탈출했는지 확인
        if len(player) == 0:
            break

        # [3] 미로 이동
        # [3-1] 한명이상의 참가자와 출구를 포함한 가장 작은 정사각형 찾기 / (r,c) 사각형 시작점 / l 사각형 크기
        r,c,l = find_square()

        # [3-2] 미로 회전
        rotate(r,c,l)

    # 정답 출력, 이동거리합과 출구 좌표
    print(ans)
    print(ey+1,ex+1)