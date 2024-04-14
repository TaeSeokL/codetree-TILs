from collections import deque
def down(y,x):
    while True:
        for dy,dx in ((1,0),(0,-1),(0,1)):
            ny, nx = y +1 + dy, x + dx

            if 0<=ny<(R+3) and 0<=nx<C:
                if board[ny][nx] > 0:
                    return y,x
            else:
                return y,x
        else:
            y = y + 1

def left(y,x,d):
    # 왼쪽으로 한칸 이동 가능한지 확인
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny = y + dy
        nx = x -1 + dx

        if 0<=ny<(R+3) and 0<=nx<C:
            if board[ny][nx] > 0:
                return y,x,d
        else:
            return y,x,d
    else:
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny = y + 1 + dy
            nx = x - 1 + dx

            if 0 <= ny < (R + 3) and 0 <= nx < C:
                if board[ny][nx] > 0:
                    return y, x, d
            else:
                return y, x, d
        else:
            y,x,d = y+1, x-1, (d-1)%4
            return y,x,d

def right(y,x,d):
    # 왼쪽으로 한칸 이동 가능한지 확인
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny = y + dy
        nx = x + 1 + dx

        if 0<=ny<(R+3) and 0<=nx<C:
            if board[ny][nx] > 0:
                return y,x,d
        else:
            return y,x,d
    else:
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny = y + 1 + dy
            nx = x + 1 + dx

            if 0 <= ny < (R + 3) and 0 <= nx < C:
                if board[ny][nx] > 0:
                    return y, x, d
            else:
                return y, x, d
        else:
            y,x,d = y+1, x+1, (d+1)%4
            return y,x,d

def move(a,d):
    oy, ox, od = 1, a, d

    while True:
        dy, dx = down(oy,ox)

        if (dy,dx) == (oy,ox):
            ly, lx, ld = left(dy,dx,od)

            if (ly,lx) == (dy,dx):
                ry, rx,rd = right(ly,lx,ld)

                if (ry,rx) == (ly,lx):
                    return ly,lx,ld
                else:
                    oy,ox,od = ry,rx,rd
                    continue
            else:
                oy,ox,od = ly,lx,ld
                continue
        else:
            oy,ox = dy,dx
            continue

def move_robot(y,x,num):
    global ans

    dq = deque()
    check = [[0]*C for _ in range(R+3)]

    dq.append((y,x,num))
    check[y][x] = 1

    max_row = y
    while dq:
        y,x,n = dq.popleft()

        if y > max_row:
            max_row = y

        ey,ex = exit[n]
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            # 로봇이 이동가능한경우
            # 범위내 -> 자기우주선일 경우 or 다른우주선인데 출구좌표일경우
            if 0<=ny<(R+3) and 0<=nx<C and check[ny][nx] == 0:
                if board[ny][nx] == n:
                    dq.append((ny,nx,n))
                    check[ny][nx] = 1
                elif board[ny][nx] != n and board[ny][nx] > 0 and (y,x)==(ey,ex):
                    dq.append((ny, nx, board[ny][nx]))
                    check[ny][nx] = 1

    ans += max_row - 2

if __name__=='__main__':
    R,C,K = map(int,input().split())
    board = [[0]*C for _ in range(R+3)]

    dir = [(-1,0),(0,1),(1,0),(0,-1)]
    exit = [0]
    ans = 0

    for num in range(1,K+1):
        c, d = map(int,input().split())
        c = c-1

        y,x,d = move(c,d)       # 중앙 좌표랑 출구방향

        # 맵에 표시하기
        board[y][x] = num
        for dy,dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny,nx = y + dy, x + dx
            board[ny][nx] = num
        # 출구
        ey ,ex = y + dir[d][0], x + dir[d][1]
        exit.append((ey,ex))

        # 금지구역확인
        flag = 0
        for r in range(3):
            for c in range(C):
                if board[r][c] != 0:
                    flag = 1
                    board = [[0] * C for _ in range(R + 3)]
                    break
                if flag == 1:
                    break

        if flag == 0:
            move_robot(y,x,num)

    print(ans)