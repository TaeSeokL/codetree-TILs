if __name__=='__main__':
    n = int(input())        # 맵 크기 / n*n 학생수

    order_li = []           # 탑승순서와 좋아하는 학생
    for _ in range(n*n):
        li = list(map(int,input().split()))         # 순서대로 입력받고 저장
        order_li.append(li)
    board = [[0]*n for _ in range(n)]               # 맵

    for li in order_li:
        num, like_stu = li[0], li[1:5]      # 탑승시킬 학생과 그 학생이 좋아하는 학생
        pos = []                            # 가장 적합한 자리를 찾기 위한 배열 [행, 열, 좋아하는 학생수, 빈칸수]

        for r in range(n):
            for c in range(n):
                if board[r][c] == 0:
                    temp = [r,c,0,0]
                    for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):
                        nr, nc = r + dy, c + dx

                        if 0<=nr<n and 0<=nc<n:             # 범위내일때
                            if board[nr][nc] in like_stu:   # 좋아하는 학생있을때
                                temp[2] += 1
                            elif board[nr][nc] == 0:        # 빈칸일때
                                temp[3] += 1

                    pos.append(temp)                        # 위치 후보 추가

        # 들어갈 수 있는 위치 후보들을 우선순위에 맞게 정렬해주고, 젤 적합한 곳에 학생 넣기
        pos.sort(key=lambda x:(-x[2],-x[3],x[0],x[1]))
        board[pos[0][0]][pos[0][1]] = num

    # 학생 번호순대로 정렬
    order_li.sort(key=lambda x:x[0])
    ans = 0
    for r in range(n):
        for c in range(n):
            num = board[r][c]
            cnt = 0
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):   # 인접한 곳 체크
                nr, nc = r + dy, c + dx

                if 0 <= nr < n and 0 <= nc < n:
                    # 좋아하는 학생이 앉아있을때 몇명인지 세기
                    # 학생 번호가 1번부터 시작이고 order_li 인덱스는 0번부터 시작이므로 이렇게 조건문 작성
                    if board[nr][nc] in order_li[num-1][1:5]:
                        cnt += 1

            if cnt > 0:                                         # 1명 이상 앉아있을때 점수 집계
                ans += 10**(cnt-1)
    print(ans)