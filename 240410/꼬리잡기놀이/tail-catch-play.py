from collections import deque
def move_team():
    # 팀번호와 팀배열 꺼내오기
    for team_n,team in teams.items():
        temp = team
        # [1] 꼬리부터 삭제 / 경로로 재설정
        y,x = temp.pop()
        board[y][x] = 4

        # [2] 머리 위치에서 한칸 탐색
        y,x = temp[0]
        for d in range(4):
            ny = y + dir[d][0]
            nx = x + dir[d][1]
            # 범위내 / 경로
            if 0<=ny<n and 0<=nx<n and board[ny][nx] == 4:
                board[ny][nx] = team_n      # 맵에표시
                temp.insert(0,(ny,nx))        # 머리삽입
                teams[team_n] = temp
                break

def throw_ball(round):
    global ans

    round = round%(4*n)         # 4n 이후 초기화
    mock = round//n
    namugi = round%n

    if mock == 0:       # 공진행방향 : 왼쪽 -> 오른쪽
        for x in range(n):
            if board[namugi][x] > 4:                    # 사람 맞았을때
                hit_ball(namugi,x)
                return
    elif mock == 1:     # 공진행방향 : 아래쪽 -> 위쪽
        for y in range(n-1,-1,-1):
            if board[y][namugi] > 4:
                hit_ball(y,namugi)
                return
    elif mock == 2:     # 공진행방향 : 오른쪽 -> 왼쪽
        for x in range(n-1,-1,-1):
            if board[namugi][x] > 4:
                hit_ball(namugi,x)
                return
    else:               # 공진행방향 : 위쪽 -> 아래쪽
        for y in range(0,n):
            if board[y][namugi] > 4:
                hit_ball(y,namugi)
                return

def hit_ball(y,x):
    global ans

    team_n = board[y][x]                # 그사람 팀번호 가져오기
    temp = teams[team_n]                # 팀배열
    idx = temp.index((y, x))            # 그사람 몇번째인지 확인하기
    ans += (idx + 1) ** 2               # 정답 갱신하기
    temp.reverse()                      # 머리꼬리체인지
    teams[team_n] = temp                # 갱신

if __name__=='__main__':
    n,m,k = map(int,input().split())                            # n 맵크기 / m 팀개수 / k 라운드수
    board = [list(map(int,input().split())) for _ in range(n)]  # 초기맵정보 / 1머리 2 중간 3꼬리 / 4 이동선
    dir = [(-1,0),(1,0),(0,-1),(0,1)]                           # 방향(상하좌우)

    ans = 0             # 정답변수(점수총합)
    teams = {}          # 팀별로 사람들 위치 저장하는 딕셔너리
    team_number = 5     # 팀별 번호

    # [1] 머리사람 찾아서 팀별로 딕셔너리에 저장해주기
    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:    # 머리사람 찾았을때
                temp = [(r,c)]      # 팀별 사람 위치 리스트 = 머리 -> 중간 -> 꼬리 순으로 저장

                # 탐색큐와 방문배열
                dq = deque()
                check = [[0] * n for _ in range(n)]

                dq.append((r,c))
                check[r][c] = 1

                while dq:
                    y,x = dq.popleft()

                    for d in range(4):
                        ny = y + dir[d][0]
                        nx = x + dir[d][1]
                        # 범위내 / 미방문
                        if 0<=ny<n and 0<=nx<n and check[ny][nx] == 0:
                            # 중간사람 이거나 중간사람에서 온 꼬리사람일때
                            if board[ny][nx] == 2 or (board[y][x] == 2 and board[ny][nx] == 3):
                                dq.append((ny,nx))
                                check[ny][nx] = 1

                                temp.append((ny,nx))

                # 팀정보 저장 / 배열에 표시
                teams[team_number] = temp
                for y,x in temp:
                    board[y][x] = team_number
                team_number += 1

    # [2] 라운드 진행
    for turn in range(k):
        # [3] 각 팀 이동
        move_team()

        # [4] 공던지기
        throw_ball(turn)

    print(ans)