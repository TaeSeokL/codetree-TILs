def move_player():
    for i in range(len(player)):
        py, px, pd = player[i]

        npy = py + player_dir[pd][0]
        npx = px + player_dir[pd][1]

        if 0 <= npy < n and 0 <= npx < n:
            if (npy, npx) != (y, x):
                player[i] = [npy, npx, pd]
        else:
            if pd == 1:
                pd = 2
            elif pd == 2:
                pd = 1
            elif pd == 3:
                pd = 4
            else:
                pd = 3

            npy = py + player_dir[pd][0]
            npx = px + player_dir[pd][1]

            if 0 <= npy < n and 0 <= npx < n:
                if (npy, npx) != (y, x):
                    player[i] = [npy, npx, pd]

def start_catch(y,x):
    global ans
    temp = [(y, x)]
    for _ in range(2):
        y, x = y + dir[d][0], x + dir[d][1]
        if 0 <= y < n and 0 <= x < n:
            temp.append((y, x))

    cnt = 0
    for i in range(len(player) - 1, -1, -1):
        py, px, pd = player[i]
        if (py, px) in temp and (py, px) not in tree:
            player.pop(i)
            cnt += 1

    ans += cnt * turn

if __name__=='__main__':
    n,m,h,k = map(int,input().split())          # n 격자 크기 / m 도망자 수 / h 나무 수 / k 턴수
    # player_board = [[0]*n for _ in range(n)]
    player = []
    player_dir = [0,(0,-1),(0,1),(-1,0),(1,0)]
    tree = []

    for _ in range(m):
        y,x,d = map(int,input().split())
        if d == 1:
            # player_board[y-1][x-1] = 2
            player.append([y-1,x-1,2])
        else:
            # player_board[y-1][x-1] = 4
            player.append([y-1,x-1,4])

    for _ in range(h):
        y,x = map(int,input().split())
        tree.append((y-1,x-1))

    dir = [(-1,0),(0,1),(1,0),(0,-1)]
    ans = 0
    y,x = n//2, n//2
    length = 2
    step = 0
    flag = 0
    d = 0
    turn = 1

    while True:
        # 바깥쪽으로 나가는 달팽이
        while True:
            # 도망자 이동
            move_player()

            # 술래 이동
            ny = y + dir[d%4][0]
            nx = x + dir[d%4][1]

            step += 1
            if step == length // 2:
                d += 1
            elif step == length :
                d += 1
                step = 0
                flag = 1
            if flag == 1:
                length += 2
                flag = 0

            y, x = ny,nx

            # 술래 이동 완료, 감시 시작
            # 잡을 수 있는 위치 구하기
            start_catch(y,x)

            # 플레이어 다 죽었는지 확인
            if not player:
                print(ans)
                exit(0)

            turn += 1

            if (y,x) == (0,0):
                d = 2
                break

            if turn == k + 1 :
                print(ans)
                exit(0)

        # (0,0) -> (n-1,0) 까지 오는 일직선 달팽이
        while turn < k+1:
            # 도망자 이동
            move_player()

            # 술래이동
            ny = y + dir[d][0]
            nx = x + dir[d][1]

            y, x = ny,nx

            start_catch(y,x)

            # 플레이어 다 죽었는지 확인
            if not player:
                print(ans)
                exit(0)

            turn += 1

            if (y,x) == (n-1,0):
                length = 2 * n - 2
                step = 0
                flag = 0
                d = 1
                break
            if turn == k + 1 :
                print(ans)
                exit(0)

        # (n-1,0) -> (n//2, n//2) 까지 오는 말려들어가는 달팽이
        while turn < k + 1:
            # 도망자 이동
            move_player()

            ny = y + dir[d%4][0]
            nx = x + dir[d%4][1]

            step += 1

            if step == length//2:
                d -= 1
            elif step == length:
                d -= 1
                step = 0
                flag = 1

            if flag == 1:
                length -= 2
                flag = 0

            y, x = ny ,nx

            start_catch(y, x)

            # 플레이어 다 죽었는지 확인
            if not player:
                print(ans)
                exit(0)

            turn += 1

            if (y,x) == (n//2,n//2):
                length = 2
                step = 0
                flag = 0
                d = 0
                break
            if turn == k + 1 :
                print(ans)
                exit(0)