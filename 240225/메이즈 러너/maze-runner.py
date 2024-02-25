def move_person():
    global ans
    # 참가자별 이동
    for i in range(m):
        # 참가자가 살아있을때
        # 현재 위치와 출구까지의 거리 받아오기
        if person[i]:
            py,px = person[i]
            pd = abs(py-ey) + abs(px-ex)
            # 상하좌우 돌며 이동가능한 곳 찾기
            for d in range(4):
                ny = py + dir[d][0]
                nx = px + dir[d][1]
                nd = abs(ny-ey) + abs(nx-ex)
                # 범위내이고 벽이 아니어야함.
                if 0<=ny<n and 0<=nx<n and board[ny][nx] == 0:
                    # 만약 다음좌표가 탈출구일때 참가자 죽이고 브레이크
                    if ny == ey and nx == ex:
                        ans += 1
                        person[i] = False
                        break
                    # 이동 후 출구와의 거리가 더 작을때 -> 이동
                    elif pd > nd :
                        person[i] = (ny,nx)
                        ans += 1
                        break

    # 참가자 모두 탈출했는지 확인
    for i in range(m):
        # 참가자 중 한명이라도 살았으면 브레이크
        if person[i]:
            break
    else:
        # 참가자 모두 탈출
        print(ans)
        print(ey+1,ex+1)
        exit(0)

def choose_square():
    global sy,sx,square_size

    # 정사각형 크기 (2~n)까지 될 수 잇음. (y1,x1) => 정사각형 좌상단 윙치 (y2,x2) => 정사각형 우하단 위치
    for sz in range(2,n+1):
        for y1 in range(n-sz+1):
            for x1 in range(n-sz+1):
                y2 = y1 + sz -1
                x2 = x1 + sz -1

                # 구한 정사각형 범위내에 출구 있는지 확인
                if not ( x1 <= ex <= x2 and y1 <= ey <= y2):
                    continue

                # 구한 정사각형 범위내에 참가자 한명 이상 있는지 확인
                is_person_in = False
                for i in range(m):
                    if person[i]:
                        py,px = person[i]
                        if x1 <= px <= x2  and y1 <= py <= y2:
                            is_person_in = True
                            break

                # 조건 충족시 정사각형 좌상단 좌표와 크기를 갱신
                if is_person_in:
                    sy, sx, square_size = y1, x1, sz
                    return

def rotate_square():
    global ey, ex
    # 정사각형 내부 벽들의 내구도 까기
    for i in range(sy,sy+square_size):
        for j in range(sx,sx+square_size):
            if board[i][j] != 0:
                board[i][j] -= 1

    # 정사각형 회전
    for y in range(sy,sy+square_size):
        for x in range(sx,sx+square_size):
            # (sy,sx)부터 시작하는 기준점을 (0,0)으로 옮기기 위해 기준점 변환
            oy, ox = y - sy, x - sx

            # (0,0)에서 90' 회전하면 이렇게 됨. (y,x) -> (x,n-y-1)
            ry = ox
            rx = square_size-oy-1

            # 다시 기준점 변환
            ry = ry + sy
            rx = rx + sx

            # 저장해놓음
            next_board[ry][rx] = board[y][x]

    # 계산한 값 옮겨주기
    for y in range(sy,sy+square_size):
        for x in range(sx,sx+square_size):
            board[y][x] = next_board[y][x]

    # 벽을 회전시켰으니 탈출구와 참가자들도 정사각형에 포함되는지 확인하고 포함되면 회전시켜준다.
    # 참가자 회전
    for i in range(m):
        if person[i]:
            py, px = person[i]
            if sy<=py<(sy+square_size) and sx<=px<(sx+square_size):
                # 변환
                oy, ox = py -sy, px - sx
                # 회전
                ry, rx= ox, square_size-oy-1
                # 변환
                ry, rx= ry+sy, rx + sx

                person[i] = (ry,rx)

    # 출구 회전
    if sy<=ey<(sy+square_size) and sx<=ex<(sy+square_size):
        # 변환
        oy, ox = ey - sy, ex - sx
        # 회전
        ry, rx = ox, square_size - oy - 1
        # 변환
        ry, rx= ry + sy, rx + sx

        ey, ex = ry, rx

if __name__=='__main__':
    n,m,k = map(int,input().split())                            # n 맵크기, m 참가자수, k 게임시간

    board = [list(map(int,input().split())) for _ in range(n)]  # 맵 정보
    next_board = [[0]*n for _ in range(n)]                      # 계산을 편하게 하기 위한 임시 저장배열
    person = []                                                 # 참가자 위치배열
    for i in range(m):
        a,b = tuple(map(int, input().split()))
        a,b = a-1,b-1
        person.append((a,b))

    ey ,ex = tuple(map(int,input().split()))                    # 출구 위치
    ey, ex = ey -1, ex -1
    sy, sx, square_size = 0,0,0                                 # 정사각형 관련 변수
    dir = [(-1,0),(1,0),(0,-1),(0,1)]                           # 이동 변수
    ans = 0                                                     # 참가자 이동 거리 합

    for time in range(k):
        # 참가자 이동
        move_person()
        # 정사각형 선택
        choose_square()
        # 정사각형 회전
        rotate_square()

    print(ans)
    print(ey+1,ex+1)