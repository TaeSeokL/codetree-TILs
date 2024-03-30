from collections import deque

# 머리 좌표와 팀번호를 입력받아서 팀 정보 저장와 배열 처리를 해주는 함수
def bfs(sy,sx,team_n):
    dq = deque()                            # 탐색큐
    check = [[0]*n for _ in range(n)]       # 방문 배열
    team = []                               # 전달받은 머리를 포함하는 팀배열

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

# 팀 이동 시켜주는 함수
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

# 공 던지는 함수
def throw_ball(round):
    global ans
    # [1] 공 시작 위치 구하기
    round = round%(4*n)             # round가 4n마다 초기화 되므로 이렇게 처리

    if round//n == 0:               # 오른쪽으로 가는 공 / round를 n으로 나눈 몫이 0
        by, bx = round%n, 0         # 공 시작 위치 처리
        bd = 0                      # 공 진행방향
    elif round//n == 1:             # 위쪽으로 가는 공 / round를 n으로 나눈 몫이 1
        by, bx = n - 1, round % n
        bd = 1
    elif round//n == 2:             # 왼쪽으로 가는 공 / round를 n으로 나눈 몫이 2
        by, bx = n-1- round% n, n - 1
        bd = 2
    else:                           # 아래쪽으로 가는 공 / round를 n으로 나눈 몫이 3
        by, bx = 0, n - 1 - round % n
        bd = 3

    # [2] 공 방향으로 n만큼 던지기
    for _ in range(n):
        if board[by][bx] > 4:                   # 사람 발견한 경우
            tnum = board[by][bx]                # 발견한 사람의 팀 번호 받기
            idx = teams[tnum].index((by,bx))    # 발견한 사람이 팀내에서 몇번째 위치하는지 확인
            ans += (idx+1) ** 2                 # 정답 갱신
            teams[tnum].reverse()               # 공 맞은 팀 머리 꼬리 바꿔주기
            return
        else:                                   # 사람 없을경우 계속 진행
            by, bx = by + ball_dir[bd][0], bx + ball_dir[bd][1]

if __name__=='__main__':
    n, m, k = map(int,input().split())                            # n 격자 크기 / m 팀 갯수 / k 라운드 수

    board = [list(map(int,input().split())) for _ in range(n)]    # 격자 정보
    ball_dir = [(0,1),(-1,0),(0,-1),(1,0)]                        # 공 방향 / 우 상 좌 하
    ans = 0

    team_number = 5                         # 팀 번호 변수
    teams = {}                              # 팀별로 위치저장 딕셔너리

    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:            # 배열 전체 순회하다 머리 발견시에 bfs 타주기
                bfs(r,c,team_number)
                team_number += 1            # bfs 통해서 방금 머리의 팀정보를 전부 저장했으니 팀번호 늘려주기


    for round in range(k):
        # [1] 팀 이동
        move_player()

        # [2] 공 던지기 구현
        throw_ball(round)

    print(ans)
