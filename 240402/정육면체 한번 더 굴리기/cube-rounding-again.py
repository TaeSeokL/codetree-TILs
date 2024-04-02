from collections import deque
# 점수 얻는 BFS
def bfs(y,x,v):
    global ans
    dq = deque()                            # 탐색 큐
    check = [[0]*n for _ in range(n)]       # 방문 배열

    dq.append((y,x))        # 초기 위치 추가
    check[y][x] = 1         # 방문 체크
    ans += v                # 정답 누적

    while dq:
        py, px = dq.popleft()

        # 인접한 곳 탐색하기
        for dy, dx in ((-1,0),(0,1),(1,0),(0,-1)):
            yy,xx = py + dy, px + dx
            # 범위내이고 방문안했고 현재 주사위가 놓인 보드상 숫자와 같을때만 탐색 이어감 / 그리고 정답 누적
            if 0<=yy<n and 0<=xx<n and check[yy][xx] == 0 and board[yy][xx] == v:
                dq.append((yy,xx))
                check[yy][xx] = 1
                ans += v

if __name__=='__main__':
    n,m = map(int,input().split())                                # n 격자 크기 / m 주사위 굴리는 횟수
    board = [list(map(int,input().split())) for _ in range(n)]    # 맵 정보
    ans = 0

    dir = [(-1,0),(0,1),(1,0),(0,-1)]           # 방향 / 상 우 하 좌(시계)
    d = 1                                       # 초기 주사위 방향 (우)
    n1,n2,n3,n4,n5,n6 = 1,2,3,4,5,6             # 초기 주사위 초기화
    y,x = 0,0                                   # 초기 주사위 위치

    for turn in range(m):
        # 주사위 굴리기
        ny, nx = y + dir[d][0], x + dir[d][1]

        if 0<=ny<n and 0<=nx<n:         # 범위내
            if d == 0:      # 위로 구른 경우
                n1, n2, n5, n6 = n2,n6,n1,n5
            elif d == 1:    # 오른쪽으로 구른 경우
                n1, n3, n4, n6 = n4, n1, n6, n3
            elif d == 2:    # 밑으로 구른 경우
                n1, n2, n5, n6 = n5, n1, n6, n2
            else:           # 왼쪽으로 구른 경우
                n1, n3, n4, n6 = n3, n6, n1, n4
        else:                           # 범위 밖 -> 반대 방향으로 이동
            d = (d+2)%4
            ny, nx = y + dir[d][0], x + dir[d][1]

            if d == 0:      # 위로 구른 경우
                n1, n2, n5, n6 = n2,n6,n1,n5
            elif d == 1:    # 오른쪽으로 구른 경우
                n1, n3, n4, n6 = n4, n1, n6, n3
            elif d == 2:    # 밑으로 구른 경우
                n1, n2, n5, n6 = n5, n1, n6, n2
            else:           # 왼쪽으로 구른 경우
                n1, n3, n4, n6 = n3, n6, n1, n4
        y, x = ny, nx       # 위치 갱신

        # 방향 조정
        if board[ny][nx] < n6:
            d = (d + 1) % 4  # 보드 숫자 > 주사위 밑면 : 시계 90도 회전
        elif board[ny][nx] > n6:
            d = (d - 1) % 4  # 보드 숫자 < 주사위 밑면 반시계 90도 회전

        # 점수 얻기
        bfs(y,x,board[y][x])

    print(ans)
