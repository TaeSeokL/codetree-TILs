def put_block_in_yellow(t,y,x):
    # 블럭 타입별로 처리
    if t == 1:          # 1x1 블럭
        pos = 5
        for i in range(6):
            if yellow_area[i][x] == 1:
                pos = i -1
                break
        yellow_area[pos][x] = 1
    elif t == 2:        # 1x2 블럭
        pos = 5
        for i in range(6):
                if yellow_area[i][x] == 1:
                    pos = i - 1
                    break
                elif yellow_area[i][x+1] == 1:
                    pos = i - 1
                    break
        yellow_area[pos][x], yellow_area[pos][x+1] = 1, 1
    else:               # 1x3 블럭
        pos = 5
        for i in range(6):
            if yellow_area[i][x] == 1:
                pos = i-1
                break
        yellow_area[pos][x], yellow_area[pos-1][x] = 1, 1

def put_block_in_red(t,y,x):
    if t == 1:
        pos = 5
        for j in range(6):
            if red_area[y][j] == 1:
                pos = j - 1
                break
        red_area[y][pos] = 1
    elif t == 2:
        pos = 5
        for j in range(6):
            if red_area[y][j] == 1:
                pos = j -1
                break
        red_area[y][pos], red_area[y][pos -1] = 1, 1
    else:
        pos = 5
        for j in range(6):
            if red_area[y][j] == 1:
                pos = j -1
                break
            elif red_area[y+1][j] == 1:
                pos = j -1
                break
        red_area[y][pos], red_area[y+1][pos] = 1, 1

def yellow_score():
    global ans
    row = 5     # 검사중인 행 위치

    # 진한 부분만 검사하면 됨.
    while row >= 2:
        # 만약 점수 얻을 수 있을 경우 -> 그 행 모두 0으로 만들어주고, 점수 누적
        if (yellow_area[row][0],yellow_area[row][1],yellow_area[row][2],yellow_area[row][3]) == (1,1,1,1):
            yellow_area[row][0], yellow_area[row][1], yellow_area[row][2], yellow_area[row][3] = 0,0,0,0
            ans += 1
            # 위에 블럭들을 하나씩 내려준다.
            for i in range(row,0,-1):
                for j in range(4):
                    yellow_area[i][j],yellow_area[i-1][j] = yellow_area[i-1][j],yellow_area[i][j]
        else:   # 점수 못얻을 경우 그 위의 행 조사
            row -= 1

def red_score():
    global ans
    col = 5

    while col >= 2:
        if (red_area[0][col],red_area[1][col],red_area[2][col],red_area[3][col]) == (1,1,1,1):
            red_area[0][col], red_area[1][col], red_area[2][col], red_area[3][col] = 0,0,0,0
            ans += 1

            for j in range(col,0,-1):
                for i in range(4):
                    red_area[i][j], red_area[i][j-1] = red_area[i][j-1],red_area[i][j]
        else:
            col -= 1

def yellow_forbidden():
    cnt = 0         # 삭제해야할 행 갯수
    for i in range(2):
        for j in range(4):
            if yellow_area[i][j] == 1:      # 금지 구역에 블럭잇으면 cnt누적 : 최대 2
                cnt += 1
                break
    if cnt > 0:
        # 행 삭제해주기
        row = 5
        for i in range(cnt):
            for j in range(4):
                yellow_area[row-i][j] = 0

        # 행 내려주기
        for i in range(5,cnt-1,-1):
            for j in range(4):
                yellow_area[i][j], yellow_area[i-cnt][j] = yellow_area[i-cnt][j], yellow_area[i][j]

def red_forbidden():
    cnt = 0
    for j in range(2):
        for i in range(4):
            if red_area[i][j] == 1:
                cnt += 1
                break

    if cnt > 0:
        col = 5
        for j in range(cnt):
            for i in range(4):
                red_area[i][col-j] = 0

    for j in range(5,cnt-1,-1):
        for i in range(4):
            red_area[i][j], red_area[i][j-cnt] = red_area[i][j-cnt], red_area[i][j]

if __name__=='__main__':
    k = int(input())                            # 블럭 입력 횟수
    yellow_area = [[0]*4 for _ in range(6)]     # 노란 영역
    red_area = [[0]*6 for _ in range(4)]        # 빨간 영역
    ans = 0                                     # 정답변수

    for turn in range(k):
        t, y, x = map(int,input().split())

        # [1] 블럭 쌓기
        put_block_in_yellow(t,y,x)
        put_block_in_red(t, y, x)

        # [2] 꽉찬 부분 없애고 점수 얻기
        yellow_score()
        red_score()

        # [3] 연한 부분에 블럭 있는지 확인 후 삭제 후 배열 정리
        yellow_forbidden()
        red_forbidden()
    
    # 정답 구하기
    res = 0
    for r in range(6):
        for c in range(4):
            if yellow_area[r][c] == 1:
                res += 1

    for r in range(4):
        for c in range(6):
            if red_area[r][c] == 1:
                res += 1

    print(ans)
    print(res)