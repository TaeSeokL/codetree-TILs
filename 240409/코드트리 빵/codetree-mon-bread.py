from collections import deque

def move_person():
    forbidden_area = []
    for num in range(1,m+1):        # 사람의 번호대로 돌아줌
        if person[num]:             # 사람이 격자내에 존재하는 경우만 이동
            sy, sx = store[num]     # 그 사람이 가야하는 편의점 좌표
            py, px = person[num]    # 그 사람의 현재 위치

            # [1] 사람 -> 편의점 최단경로 찾기 / BFS + 경로
            dq = deque()
            check =[[0]*n for _ in range(n)]

            # 초기 데이터 넣어주기 및 방문처리 (현재사람위치)
            dq.append((py,px,[]))
            check[py][px] = 1

            while dq:
                y,x,lst = dq.popleft()

                for dy,dx in ((-1,0),(0,-1),(0,1),(1,0)): # 방향우선수위(상좌우하)순으로 경로 탐색
                    ny = y + dy
                    nx = x + dx
                    # 범위내 / 미방문 / 금지구역 x
                    if 0<=ny<n and 0<=nx<n and check[ny][nx] == 0 and board[ny][nx] != -1:
                        # 편의점 도착했을때 -> 사람 원래 위치 지워주고 위치 갱신 후 맵에 표시
                        if (ny, nx) == (sy, sx):
                            dboard[py][px].remove(num)  # 디버깅용 위치표시

                            if lst:                   # 이동 경로가 있을때 : 즉 한칸 이상 거쳐서 편의점 도착시
                                person[num] = lst[0]  # 이동한 경로의 젤 처음 이동위치로 사람 위치 갱신(한칸이동)
                                yy, xx = person[num]
                            else:                     # 이동 경로가 없을떄 : 즉 한칸 이동으로 바로 편의점 도착시
                                yy, xx = sy, sx

                            # 만약 이동한 그위치가 편의점일때
                            if (yy, xx) == (sy, sx):
                                forbidden_area.append((sy, sx))  # 금지구역처리를 위해 위치 저장
                                person[num] = False  # 사람 도착 처리
                            # 그냥 빈칸일때
                            else:
                                dboard[yy][xx].append(num)  # 디버깅용 위치표시
                            dq.clear()
                            break
                        # 금지구역 아닐때 계속 탐색 진행
                        dq.append((ny,nx,lst+[(ny,nx)]))
                        check[ny][nx] = 1

    # [2] 사람이 모두 이동하고 금지구역 처리
    if forbidden_area:
        for i in range (len(forbidden_area)):
            y,x = forbidden_area[i]
            board[y][x] = -1

def add_person(num):
    temp = []               # 베캠 후보 저장
    sy, sx = store[num]     # t번 사람이 가고 싶은 편의점 위치

    # [1] 편의점 -> 베캠 탐색
    dq = deque()
    check = [[0] * n for _ in range(n)]

    # 초기 데이터 넣어주기 및 방문처리 (현재편의점위치)) 거리값추가
    dq.append((sy, sx,0))
    check[sy][sx] = 1

    while dq:
        y,x,L = dq.popleft()

        for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):  # 상좌우하 순 탐색
            ny = y + dy
            nx = x + dx
            # 범위내 / 미방문 / 금지구역 x
            if 0 <= ny < n and 0 <= nx < n and check[ny][nx] == 0 and board[ny][nx] != -1:
                # 만약 다음 위치가 베이스 캠프면 후보 저장
                if board[ny][nx] == 1:
                    temp.append((ny,nx,L+1))
                else:
                    dq.append((ny,nx,L+1))
                    check[ny][nx] = 1

    # 베이스캠프 : 행작 -> 열작 순서 정렬
    temp.sort(key=lambda x:(x[2],x[0],x[1]))
    ny, nx,_ = temp[0]                  # t번 사람이 이동하는 베이스캠프 위치
    person[num] = (ny, nx)              # 위치갱신
    dboard[ny][nx].append(num)          # 디버깅용 위치 표시
    board[ny][nx] = -1                  # 금지구역지정

if __name__=='__main__':
    n,m = map(int,input().split())                              # n 맵크기 / m 사람수
    board = [list(map(int,input().split())) for _ in range(n)]  # 맵정보 / 0 = 빈칸 1 = 베이스캠프
    dboard = [[[] for _ in range(n)] for _ in range(n)]         # 디버깅을 위한 맵

    # 편의점 위치 저장
    store = [0]*(m+1)     # t번 사람이 가고 싶은 편의점 위치 / 인덱스 == t
    for i in range(1, m+1):
        r,c = map(int,input().split())
        store[i] = (r-1,c-1)

    person = [False] *(m+1)   # 사람별 위치 관리 배열 / 인덱스 == t

    turn = 1        # 현재 시간
    while True:     # 사람이 모두 편의점에 도착할때 까지 무한 반복
        # [1] 격자에 있는 사람들이 각자의 편의점으로 한칸 이동
        move_person()

        # [2] 조건 확인 후 만족할때 t번사람을 베이스캠프에 넣기
        if turn <= m:
            add_person(turn)

        # [3] 사람이 전부 도착했으면 종료
        for num in range(1,m+1):
            if person[num]:     # 격자 내에 존재 시 계속 진행
                break
        else:
            print(turn)
            break

        turn += 1               # 턴 계속 진행