from copy import deepcopy
from collections import deque

# 공격자 -> 피해자 사이의 최단 경로를 찾는 함수. 명심하자. BFS는 찾으면 무조건 최단경로이다.
# 만약 이문제처럼 방향에 우선순위가 정해져있다면 그 우선순서대로 탐색하면 조건에 만족하는 최단 경로를 찾을 수 있음.
def find_min_road(ay,ax,dy,dx):
    global min_road

    # 체크 배열과 탐색 큐 정의 후 공격자 좌표 추가하고 방문체크
    check = [[0] * m for _ in range(n)]
    dq = deque()

    dq.append((ay,ax,[]))
    check[ay][ax] = 1

    # 탐색 큐가 빌때까지 탐색
    while dq:
        # 현재 탐색 위치와 경로를 pop 함.
        y,x,road = dq.popleft()

        # 만약 현재 위치가 피해자의 위치라면 그동안 저장했던 경로를 min_road에 카피해주고 함수 종료.
        if y == dy and x == dx :
            min_road = deepcopy(road)
            return

        # 방향 우선순위대로 4방향 탐색
        for yy, xx in ((0,1),(1,0),(0,-1),(-1,0)):
            # 문제에서 격자를 넘어가도 반대로 나오는 조건이 있었기때문에,
            # 다음좌표를 업데이트 후 y좌표는 n, x좌표는 m으로 나머지 연산을 처리해서 격자를 벗어나는 것을 처리
            ny, nx = y + yy, x + xx
            ny,nx = ny%n, nx%m

            # 만약 다음 위치의 포탑이 살아있고, 방문을 안했다면 탐색큐에 추가함.
            # 이때 위에서 pop한 경로에 다음 위치를 더해서 쭉 경로를 저장해줌.
            if board[ny][nx] > 0 and check[ny][nx] == 0:
                dq.append((ny,nx,road + [(ny,nx)]))
                check[ny][nx] = 1

if __name__=='__main__':
    n, m, k = map(int,input().split())                          # n x m 격자 크기, k 턴 수
    board = [list(map(int,input().split())) for _ in range(n)]  # 맵정보
    attack_turn = [[0]*m for _ in range(n)]                     # 포탑별 최근 공격한 턴 저장
    total_potop = 0                                             # 포탑 남은 갯수 체크 변수

    # 포탑 갯수 세기
    for r in range(n):
        for c in range(m):
            if board[r][c] != 0:
                total_potop += 1

    # 턴수만큼 게임 진행
    for turn in range(1,k+1):
        # 1. 공격자와 피해자 선정 : 완전 탐색 + 다중정렬
        temp = []               # 공격자, 피해자가 될 수 있는 포탑 저장 배열
        related_attack = []     # 공격에 영향 받은 포탑들 위치 저장 배열

        # 후보들 찾기 == 공격력이 0이 아닌 모든 포탑, (위치, 행과열의 합, 현재 공격력, 마지막으로 공격한 턴) 형식으로 저장
        for r in range(n):
            for c in range(m):
                if board[r][c] != 0:
                    temp.append((r,c,r+c,board[r][c],attack_turn[r][c]))

        # 후보들을 우선순위 기준으로 정렬
        # 공격력 가장 낮은 -> 가장 최근에 공격 -> 행과 열 합이 가장 큰 -> 열이 가장 큰
        temp.sort(key=lambda x:(x[3],-x[4],-x[2],-x[1]))

        # 정렬 후 맨앞이 공격자 -> 문제 조건에 따라 공격력을 늘려줌.
        # 최근 공격한 턴을 현재 턴으로 업데트 시켜주고, 공격에 영향을 받았다는것을 저장해줌.
        attack_y, attack_x,_,_,_ = temp[0]
        board[attack_y][attack_x] += n+m
        attack_turn[attack_y][attack_x] = turn
        related_attack.append((attack_y,attack_x))

        # 맨 뒤가 피해자, 공격에 영향 받았다는 것 저장
        damage_y, damage_x,_,_,_ = temp[-1]
        related_attack.append((damage_y,damage_x))

        # 최단경로 찾기, 공격자와 피해자의 좌표를 전달
        min_road = []
        find_min_road(attack_y,attack_x,damage_y,damage_x)

        # 최단 경로 존재 => 레이저 공격 / 존재 안함 -> 포탄 공격
        if min_road:
            # 경로에 있는 놈들 공격
            for i in range(len(min_road)-1):
                ry, rx = min_road[i]
                if board[ry][rx] > 0 :
                    board[ry][rx] -= board[attack_y][attack_x]//2
                    related_attack.append((ry,rx))

                    # 만약 포탑이 죽었을때 처리해줌.
                    if board[ry][rx] <= 0:
                        board[ry][rx] = 0
                        total_potop -= 1

            # 피해자 공격
            board[damage_y][damage_x] -= board[attack_y][attack_x]
        else:
            # 포탄 공격
            # 피해자 공격
            board[damage_y][damage_x] -= board[attack_y][attack_x]

            # 주위 8방향 데미지
            for dy,dx in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)):
                ny, nx = damage_y + dy, damage_x + dx
                ny, nx = ny%n, nx%m

                # 공격자는 포탄 범위 공격에 영향을 받지 않으므로 조건문 추가
                if (ny,nx) != (attack_y,attack_x) and board[ny][nx] > 0:
                    related_attack.append((ny,nx))
                    board[ny][nx] -= board[attack_y][attack_x]//2

                    # 죽은 포탑 처리
                    if board[ny][nx] <= 0:
                        board[ny][nx] = 0
                        total_potop -= 1

        # 피해자 죽었을 경우 처리
        if board[damage_y][damage_x] <= 0:
            board[damage_y][damage_x] = 0
            total_potop -= 1

        # 하나의 턴을 진행하고 살아남은 포탑이 한개라면 그 즉시 게임 종료.
        if total_potop == 1:
            for r in range(n):
                for c in range(m):
                    if board[r][c] != 0:
                        print(board[r][c])
                        exit(0)

        # 포탑 정비 = 공격에 영향을 받지 않고, 살아있는 포탑들만 공격력 +1
        for r in range(n):
            for c in range(m):
                if board[r][c] != 0 and (r,c) not in related_attack:
                    board[r][c] += 1

    # 모든 턴이 종료된 후 최대 공격력을 찾기
    max_val = -100
    for x in board:
        row_max_val = max(x)
        max_val = max(max_val,row_max_val)
    print(max_val)

