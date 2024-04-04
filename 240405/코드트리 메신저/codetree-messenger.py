# 11:10 - 12:12 -- 12:36 코드고민
# 09:55 - 11:08
# 트리구조
# 인덱스가 자식이고 값이 부모인 구조
# 매 명령마다 자식 기준으로 부모까지 갈 수 있는지 보면 10e6*10e6 이라서 무조건 시간초과
# 전체 트리를 부모 기준으로 입력받아서 저장해야 함
# 65%에서 시간초과
# 이것도 depth가 0인 0에서부터 시작한다고 가정했을 때 굉장히 비효율적임
# Depth 맥스 값이 20이다 - 반띵해서 2e10~10e3!!!!!! ---안돼..
# 처음에 depth값에 대한 모든 경우들을 저장해두기
# 거기서만 탐색하기! 인덱스 나누고 하면 금방 할 듯?
# 찾으려는 것
# 특정 노드까지 갈 수 있는 모든 경우의 수 계산
# 업데이트가 어려워짐
# 토론창에 dp 쓰는거라고 해서 답지 봤는데 그건 아니고 마지막에 직접 생각한 방법이랑 크게 다르지 않음..
# 자식 노드 돌아보는 순간 망함 parent로 올라가는 것만 생각하기
#
from collections import deque
N, Q = list(map(int, input().split()))

def toggle_noti(c):
    global auth, message, chat_init, noti
    a = auth[c]
    cur = c
    # print(message[c])
    for j in range(a):
        par = chat_init[cur]
        if noti[c]:
            message[par][0] -= 1
        else:
            message[par][0] += 1
        cur = par
        # if noti[cur]:
            # break
    for aa, t in enumerate(message[c]):
        if aa == 0 or t == 0:
            continue
        cur = c
        for j in range(aa):
            par = chat_init[cur]
            k = aa - j - 1
            if noti[c]:
                message[par][k] -= t
            else:
                message[par][k] += t
            cur = par
            # if noti[cur]:
                # break
    noti[c] = not noti[c]  # 알람 변경

def change_power(c, power):
    a = auth[c]  # 이전 권한 세기
    cur = c
    for i in range(1, a + 1):
        # print("cur, par", cur, par)
        par = chat_init[cur]
        for j in range(a + 1 - i):
            message[par][j] -= 1
        cur = par
        # if noti[cur]:
            # break
    cur = c
    for i in range(1, power + 1):
        par = chat_init[cur]
        for j in range(power + 1 - i):
            message[par][j] += 1
        cur = par
        # if noti[cur]:
            # break
    auth[c] = power  # 권한 세기 업데이트

for q in range(Q):
    order = list(map(int, input().split()))
    # print("===================")
    # print("order",order[0])
    if order[0] == 100: # 사내 메신저 준비
        chat_init = [-1]+order[1:1+N]
        auth = [-1]+order[1+N:]
        noti = [True]*(N+1)
        # message = [0]*(N+1) # 총 알람 수
        message = [[0]*(22) for _ in range(N+1)] # 특정 depth에서 몇개가 왔는지 확인
        for c in range(1, N+1):
            a = auth[c]
            cur = c
            for j in range(1,a+1):
                par = chat_init[cur]
                for k in range(a+1-j):
                    if par==-1:
                        continue
                    message[par][k] += 1
                cur = par
                # print(c, j, k, cur, par, message)

    elif order[0] == 200: # 알림망 온오프
        ## 제일 어려움! 그 위치에서만 거슬러올라가는게 아니라 자식노드 모두 봐야 함
        c = order[1]
        toggle_noti(c)

    elif order[0] == 300: # 권한 세기 변경
        c, power = order[1:]
        change_power(c, power)

    elif order[0] == 400: # 부모 채팅방 교환
        c1, c2 = order[1:]
        bef_noti1, bef_noti2 = noti[c1], noti[c2]
        a1, a2 = auth[c1], auth[c2]
        # print("MESSAGE0", message)
        # 켜져있으면 끄고
        if bef_noti1:
            toggle_noti(c1)
        if bef_noti2:
            toggle_noti(c2)
        # print("MESSAGE1", message)
        # auth 바꿔넣기
        change_power(c1, a2)
        change_power(c2, a1)
        # print("MESSAGE2", message)
        # 교환
        chat_init[c2], chat_init[c1] = chat_init[c1], chat_init[c2]
        # 아까 껐던 애 다시 켜기
        if bef_noti1:
            toggle_noti(c1)
        if bef_noti2:
            toggle_noti(c2)
        # print("NOTI", noti)

    else: # 알람 받을 수 있는 채팅방 조회
        c0 = order[1]
        print(message[c0][0])

    # print("message", message)