# 이거 시간 오래걸림. 리팩토링해야함.

from collections import deque
# 상어 움직이고 겹치면 삭제하는 함수
def shark_moving():
    # 상어 번호순대로 반복문 돌아줌.
    # 상어가 살아있을때만 진행
    for shark_num in range(1,m+1):
        if shark[shark_num] :
            # 상어의 위치와 방향을 얻어오고, 거기에 따른 우선순위를 dir에 저장함.
            y,x,d = shark[shark_num][0],shark[shark_num][1],shark[shark_num][2]
            dir = direction[shark_num][d]

            # 우선순위의 방향대로 돌면서 다음 위치로 갈 수 있는지 판단.
            # 빈칸으로 우선 이동해야되기 때문에 빈칸을 먼저 찾아줌.
            # 상어가 한곳에 있을 수 있기때문에 + 리스트로 해줌.
            for nd in dir:
                ny, nx = y + dd[nd][0], x + dd[nd][1]
                if 0<=ny<n and 0<=nx<n :
                    if smell_board[ny][nx] == 0:
                        shark[shark_num] = [ny,nx,nd]
                        shark_board[ny][nx] += [shark_num]
                        shark_board[y][x] = []
                        break
            # 빈칸이 없다면 자기 냄새가 있는 곳으로 이동해야함.
            else:
                for nd in dir:
                    ny, nx = y + dd[nd][0], x + dd[nd][1]
                    if 0 <= ny < n and 0 <= nx < n:
                        if smell_board[ny][nx] == shark_num :
                            shark[shark_num] = [ny, nx, nd]
                            shark_board[ny][nx] += [shark_num]
                            shark_board[y][x] = []
                            break

    # 상어마다 위치를 받아서 겹치는 부분이 있으면 제일 작은애만 살려두고 나머지는 죽여줌.
    for num in range(1,m+1):
        if shark[num]:
            y,x = shark[num][0], shark[num][1]
            if len(shark_board[y][x]) > 1:
                shark_board[y][x].sort()
                while (len(shark_board[y][x]) != 1):
                    dead_shark = shark_board[y][x].pop(-1)
                    shark[dead_shark] = []

def smell(sec):
    # 원래 있던 냄새들 초 다 됐으면 처리, 원래 큐에 pop, append하며 t를 -1씩 해서 계산했지만
    #그렇게 하니까 시간초과가 남. 그래서 sec + k 를 t로 받아서 이게 현재 sec이랑 같아지면 그걸 제거해줌.
    # ex) 1초에 k=6인 냄새 남기면 7초에 0되서 없어져야함.
    L = 0
    length = len(shark_smell)
    while (L != length):
        y,x,t,num = shark_smell.popleft()
        if t == sec:
            smell_board[y][x] = 0
        else:
            smell_board[y][x] = num
            shark_smell.append((y,x,t,num))
        L += 1

    # 상어 현재 위치에 냄새남기기
    for num in range(1,m+1):
        if shark[num] :
            y,x = shark[num][0], shark[num][1]
            smell_board[y][x] = num
            shark_smell.append((y,x,k+sec,num))

if __name__=='__main__':
    n, m, k = map(int,input().split())              # n 맵크기, m 상어 수, k 냄새턴
    # shark : 상어 위치와 방향관리배열 [y,x,d]
    # shark_board : 맵 상에 상어 표시 3차원 배열
    # smell_board : 상어가 뿌린 냄새표현 [상어번호,k]
    shark = [0]*(m+1)
    shark_board = [[[] for _ in range(n)] for _ in range(n)]
    smell_board = [[0] * n for _ in range(n)]
    shark_smell = deque()
    dd = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 상어보드에 상어 넣기
    for i in range(n):
        arr = list(map(int,input().split()))
        for j in range(n):
            if arr[j] !=0:
                shark_board[i][j] = [arr[j]]

    # 상어 배열에 상어 위치 표시
    for i in range(n):
        for j in range(n):
            if len(shark_board[i][j]) != 0:
                shark[shark_board[i][j][0]] = [i,j]

    # init_d : 상어 초기 방향, 입력받고 상어 배열에 방향 추가
    init_d = list(map(int,input().split()))
    for i in range(m):
        shark[i+1] += [init_d[i]-1]

    # dircetion : 상어의 방향 우선순위 배열
    # direction[number][d] : number상어가 방향이 d일때 우선순위
    # 편하게 하기 위해 입력 받은 방향을 전부 1을 빼서 저장해줌.
    direction = [[] for _ in range(m+1)]
    for i in range(1,m+1):
        for j in range(4):
            arr = list(map(int, input().split()))
            for z in range(len(arr)):
                arr[z] -= 1
            direction[i].append(arr)
    
    # 처음에 냄새한번씩 뿌려야함
    smell(0)
    # print('------초기 상어 배열 상태------')
    # for x in shark_board:
    #     print(x)
    # print('------초기 냄새 배열 상태------')
    # for x in smell_board:
    #     print(x)

    for sec in range(1,1001):
        # 상어 이동하기
        shark_moving()

        # 냄새남기기
        smell(sec)

        # print('------%d턴------'%sec)
        # print('------%d턴 상어 배열 상태------'%sec)
        # for x in shark_board:
        #     print(x)
        # print('------%d턴 냄새 배열 상태------'%sec)
        # for x in smell_board:
        #     print(x)
        # print()

        # 1번만 남았는지 확인하기
        for i in range(1,m+1):
            if i != 1 and len(shark[i]) > 1:
                break
        else:
            print(sec)
            exit(0)

    print(-1)