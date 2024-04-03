if __name__=='__main__':
    n, m = map(int,input().split())                                 # n 격자 크기 / m 총 진행 년수
    board = [list(map(int,input().split())) for _ in range(n)]      # 초기 나무 정보
    next_board = [[0]*n for _ in range(n)]                          # 동시 처리를 위한 임시 저장 배열
    dir = [(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1)]   # 이동방향

    medi = [[n-1,0],[n-1,1],[n-2,0],[n-2,1]]      # 초기 영양제 위치
    move = []                                     # 이동 명령 정보

    for year in range(m):
        d, p = map(int,input().split())
        move.append((d,p))

    # 나무 성장 진행
    for d, p in move:
        d = d - 1
        # [1] 특수 영양제 이동
        for i in range(len(medi)):
            y, x = medi[i]

            # 격자 벗어나는 경우 반대로 나오게 구현
            ny = (y + dir[d][0]*p)%n
            nx = (x + dir[d][1]*p)%n

            # 특수 영양제가 있는 칸 나무 높이 1씩 증가
            board[ny][nx] += 1
            medi[i] = [ny,nx]

        # [2] 특수 영양제 투입 : 나무 성장(대각선만 확인)
        for i in range(len(medi)):
            y, x = medi[i]
            for dy,dx in ((-1,1),(-1,-1),(1,-1),(1,1)):
                ny, nx = y + dy, x + dx
                # 범위 내이고 대각선에 있는 나무 높이가 1 이상일때 : 동시 처리를 위해 임시저장배열에 저장
                if 0<=ny<n and 0<=nx<n and board[ny][nx] >= 1:
                    next_board[y][x] += 1

        # [3] 나무 성장 후 특수 영양제 초기화
        for i in range(len(medi)):
            y,x = medi[i]
            board[y][x] += next_board[y][x]
            next_board[y][x] = 0

        # 영양제 주입한 곳은 나무 깎으면 안되니까 temp 에 저장해두기
        # 다음 영양제 투입 위치 저장을 위해 medi 초기화
        temp = [x[:] for x in medi]
        medi = []

        # [4] 높이 2 이상인 나무 깎아서 특수 영양제 제작
        for r in range(n):
            for c in range(n):
                if [r,c] not in temp and board[r][c] >= 2:
                    board[r][c] -= 2
                    medi.append([r,c])

    ans = 0
    for x in board:
        ans += sum(x)

    print(ans)