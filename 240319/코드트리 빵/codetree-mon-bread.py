from collections import deque
def move_person(num):
    # 사람의 현재 위치와 편의점의 위치와 두 위치간 거리
    y, x = person[num]
    sy, sx = store[num]
    pd = abs(y-sy)+abs(x-sx)

    # 방향 우선순위대로 가까워지는 위치 찾기
    for dy, dx in ((-1,0),(0,-1),(0,1),(1,0)):
        ny,nx = y + dy, x + dx      # 사람의 다음 위치
        # 범위내이고, 통행금지칸이 아닐때
        if 0<=ny<n and 0<=nx<n and board[ny][nx] != -5:
            # 만약 편의점에 도착했다면 사람 상태 바꿔주고, 예비통행금지배열에 위치추가
            if ny == sy and nx == sx:
                person[num] = False
                never_can_go.append((ny,nx))
                return
            else:
                nd = abs(ny-sy)+abs(nx-sx)  # 이동 후 편의점 과의 거리
                # 만약 가까워졌다면 위치 업데이트
                if nd < pd :
                    person[num] = (ny,nx)
                    return

def find_near_base_camp(num):
    # 탐색 큐와 체크 배열 정의
    dq = deque()
    check = [[0]*n for _ in range(n)]

    # t번 편의점 위치, 탐색 변수들 초기화
    y,x = store[num]
    dq.append((y,x))
    check[y][x] = 1

    while dq:
        # 현재위치에서부터 우선순서대로 BFS돌며 제일 가까운 베캠 찾기
        y,x = dq.popleft()

        for dy,dx in ((-1,0),(0,-1),(0,1),(1,0)):
            ny, nx = y + dy, x +dx
            # 범위내, 통행금지아님, 방문안함일때 계속 탐색
            if 0<=ny<n and 0<=nx<n and board[ny][nx] != -5 and check[ny][nx] == 0:
                # 베캠 찾았을때
                if board[ny][nx] == -1 :
                    person[num] = (ny,nx)
                    board[ny][nx] = -5
                    return
                # 못찾았을때 계속 탐색
                else:
                    dq.append((ny,nx))
                    check[ny][nx] = 1

if __name__=='__main__':
    n, m = map(int,input().split())                             # n 격자크기, m 사람수
    board = [list(map(int,input().split())) for _ in range(n)]  # 맵정보

    person = [True]*(m+1)                   # 사람 관리 배열, True = 격자밖 대기상태, False = 도착, 위치 = 격자내위치
    store = [0]                             # 편의점 위치 관리 배열, 인덱스 = 편의점 번호
    for _ in range(m):
        r, c = map(int, input().split())    # (r,c) 편의점 위치
        store.append((r-1,c-1))

    # 베이스캠프 -1로 바꿔주기
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                board[i][j] = -1

    time = 1
    while True:
        # 사람이 이동 후 편의점에 도착하면 나머지 사람 모두 이동 후 그 칸을 금지 처리해야하기때문에
        # 이 배열을 정의해줌.
        never_can_go = []
        # 사람이 어디있는지 파악하며 격자내에 위치할 경우만 움직여줌.
        for i in range(1,m+1):
            if person[i] is not True and person[i] is not False:
                # 자신이 가고 싶은 편의점을 향해 최단거리로 한칸 움직임
                # 이 함수에서 편의점 도착 상황도 같이 처리
                move_person(i)

        # 사람 전부 도착했는지 여기서 확인
        for i in range(1,m+1):
            if person[i] is not False:
                break
        else:
            print(time)
            break

        if time <= m:
            # time번 사람 베이스 캠프에 집어넣기
            find_near_base_camp(time)

        # 통행금지 처리하기
        if never_can_go:
            for y,x in never_can_go:
                board[y][x] = -5

        time += 1