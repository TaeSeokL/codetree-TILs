from collections import deque

def bfs(sy,sx,team_n):
    dq = deque()                            # 탐색큐
    check = [[0]*n for _ in range(n)]       # 방문 배열
    team = []                               # 전달받은 머리를 포함하는 뱀 배열

    team.append((sy,sx))                    # 머리 좌표 추가
    board[sy][sx] = team_n                  # 머리에 팀 번호 넣기
    dq.append((sy,sx))                      # 머리 좌표 탐색 큐 추가
    check[sy][sx] = 1                       # 방문 표시

    while dq:
        y,x = dq.popleft()
        for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):      # 상하좌우 탐색
            ny = y + dy
            nx = x + dx
            # 범위내이고 미방문
            if 0<=ny<n and 0<=nx<n and check[ny][nx] == 0:
                # 다음 좌표의 값이 2 이거나, 출발점에서 오지 않았는데 좌표의 값이 3일때만 이동 가능 -> 뱀의 머리 머리에서 꼬리 순서대로
                if board[ny][nx] == 2 or ((y,x) != (sy,sx) and board[ny][nx] == 3):
                    team.append((ny,nx))        # 좌표 추가
                    board[ny][nx] = team_n      # 팀 번호 넣기
                    dq.append((ny,nx))          # 탐색 큐 추가
                    check[ny][nx] = 1           # 방문 표시

    teams[team_n] = team        # 딕셔너리에 key 값을 팀번호, value 값을 팀 위치 배열로 저장해줌.

def move_player():
    for team in teams.values():     # value(팀배열) 받아오기
        ey, ex = team.pop()         # 꼬리좌표 삭제 후
        board[ey][ex] = 4           # 경로로 재설정

        sy, sx = team[0]            # 머리 좌표 꺼내기
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            ny, nx = sy + dy, sx + dx
            # 범위내이고, 경로일때만 이동
            if 0<=ny<n and 0<=nx<n and board[ny][nx] == 4:
                team.insert(0,(ny,nx))              # 머리좌표 갱신 후 추가
                board[ny][nx] = board[sy][sx]       # 보드 상에 표시해주기(팀번호)
                break

def throw_ball(round):
    global ans

    if 1 <= round <= n:  # 오른쪽으로 가는 공
        by, bx = round - 1, 0
        bd = 0
    elif n + 1 <= round <= 2 * n:  # 위쪽으로 가는 공
        by, bx = n - 1, (round - 1) % n
        bd = 1
    elif 2 * n + 1 <= round <= 3 * n:  # 왼쪽으로 가는 공
        by, bx = n-1-(round - 1) % n, n - 1
        bd = 2
    else:  # 아래쪽으로 가는 공
        by, bx = 0, n - 1 - (round - 1) % n
        bd = 3

    # [3] 공이 던져지는 과정 구현
    for _ in range(n):
        if board[by][bx] > 4:  # 사람 발견한 경우
            tnum = board[by][bx]
            idx = teams[tnum].index((by,bx))
            ans += (idx+1) ** 2

            teams[tnum].reverse()
            return
        else:
            by, bx = by + ball_dir[bd][0], bx + ball_dir[bd][1]

if __name__=='__main__':
    n, m, k = map(int,input().split())          # n 격자 크기 / m 팀 갯수 / k 라운드 수

    board = [list(map(int,input().split())) for _ in range(n)]    # 격자 정보
    ball_dir = [(0,1),(-1,0),(0,-1),(1,0)]  # 공 방향 / 우 상 좌 하
    ans = 0

    team_number = 5
    teams = {}

    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:
                bfs(r,c,team_number)
                team_number += 1


    for round in range(1,k+1):
        # [1] 팀 이동
        move_player()

        # [2] 공 던지기 구현
        throw_ball(round)

    print(ans)