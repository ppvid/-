#수송문제
#공급하는 양은 공급 능력을 초과할 수 없음
#공급량은 수요량보다 커야함

#예제1_수송문제
#i: 생산한 달, j:설치한 달
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
x={}
for i in range(4):
    for j in range(4):
        if i<=j:
            x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
limit=[25,35,30,10]
demands=[10,15,25,20]
cost=[1.08,1.11,1.1,1.13]
for i in range(4):
    solver.Add(sum(x[i,j] for j in range(4) if j>=i)<=limit[i])
for j in range(4):
    solver.Add(sum(x[i,j] for i in range(4) if i<=j)>=demands[j])
#목적함수
con=[]
for i in range(4):
    for j in range(4):
        if i<=j:
            con.append((cost[i]+0.015*(j-i))*x[i,j])
solver.Minimize(sum(con))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'Total cost = {solver.Objective().Value():.1f}')
    for i in range(4):
        for j in range(4):
            if i<=j:
                print(x[i,j].name(),':',x[i,j].solution_value())
#위의 코드는 제약 조건들을 부등호로 표현했으나 수송 문제의 표준형은 더미 도착지를 만들어 등호로 제약 조건을 설정하는 것이다
#수송문제 표준형은 공급량=수요량이다. 나중에 더미 변수로 간 값들을 보고 해석이 더 용이해지는 등의 이점이 있다

#예제2_with 더미 수요지
M=1000000
data=[[16,16,13,22,17],
      [14,14,13,19,15],
      [19,19,20,23,M],
      #더미 변수에서 선택되면 나머지 수요지에서 가는 값들이 우선순위가 밀리는 것임
      #무조건 할당 되어야 하는 최솟값 범위일 시 bigM 넣고 여분이 들어가는 열에 0 넣기
      [M,0,M,0,0]]
supplies=[50,60,50,50]
demands=[30,20,70,30,60]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
x={}
for i in range(4):
    for j in range(5):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
#공급략
for i in range(4):
    solver.Add(sum(x[i,j]for j in range(5))==supplies[i])
#수요량
for j in range(5):
    solver.Add(sum(x[i,j] for i in range(4))==demands[j])
solver.Minimize(sum(data[i][j]*x[i,j] for i in range(4) for j in range(5)))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('Total Cost= ',solver.Objective().Value())
    for i in range(3):
        for j in range(5):
            print(x[i,j].name(),':',x[i,j].solution_value())

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#예제3_(1)수송문제 with 더미 수요지
#한 제품을 두개 이상 공장에서 생산할 수 있는 경우
M=1000000
data=[[41,27,28,24,0],
      [40,29,M,23,0],
      [37,30,27,21,0]
      ]
demands=[20,30,30,40,75]
supplies=[75,75,45]

x={}
for i in range(3):
    for j in range(5):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
#공급량 공급한도
for i in range(3):
    solver.Add(sum(x[i,j] for j in range(5))==supplies[i])
#공급량=수요량
for j in range(5):
    solver.Add(sum(x[i,j] for i in range(3))==demands[j])
solver.Minimize(sum(data[i][j]*x[i,j] for i in range(3) for j in range(5)))
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
     print(f'Total cost = {solver.Objective().Value():.1f}')
     for i in range(3):
         for j in range(4):
             print(x[i,j].name(),':',x[i,j].solution_value())
#(2)한가지 제품이 한가지 공장에서만 생산되는 경우(할당문제)
#(2)-1번 풀이_BIGM 도입
y={}
for i in range(3):
    for j in range(5):
        y[i,j]=solver.BoolVar(f'y[{i},{j}]')
for j in range(5):
    solver.Add(sum(y[i,j] for i in range(3))==1)
for i in range(3):
    for j in range(4):
        #bigM 도입
        solver.Add(x[i,j]<=y[i,j]*M)
solver.Minimize(sum(data[i][j]*x[i,j] for i in range(3) for j in range(5)))
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
     print(f'Total cost = {solver.Objective().Value():.1f}')
     for i in range(3):
         for j in range(4):
             print(x[i,j].name(),':',x[i,j].solution_value())

#(2)-2번 풀이_with 더미도착지_수송문제
#데이터 값을 비용으로 채워 넣는다>데이터값*수요
#공급능력을 보고 2개 이상 생산 가능한 공장의 행을 하나 늘린다
#표의 각 셀마다 이진변수 부여하고 열,행 합이 1이 되도록 제약식 건다

#예제3번_할당문제를 수송문제로
from ortools.graph.python import min_cost_flow
#SimpleMinCostFlow>smcf
smcf=min_cost_flow.SimpleMinCostFlow()
#공급노드
start_nodes=(
    [0,0,0,0]+[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]+[5,6,7,8]
)
#수요노드
end_nodes =(
    [1,2,3,4]+[5,6,7,8,5,6,7,8,5,6,7,8,5,6,7,8]+[9,9,9,9]
)
#비용
cost=([0,0,0,0]+[90,76,75,70,35,85,55,65,125,95,90,105,45,110,95,115]+[0,0,0,0])
#의사결정 변수의 최댓값, 할당 문제이므로 이진변수를 사용해 1이 된다
capacity=([1,1,1,1]+[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]+[1,1,1,1])
source=0
sink=9
#할당해야 할 작업 수
task=4
supplies=[task,0,0,0,0,0,0,0,0,-task]
#각 가지의 그리기
for i in range(len(start_nodes)):
    smcf.add_arc_with_capacity_and_unit_cost(
        start_nodes[i],end_nodes[i],capacity[i],cost[i]
    )
#각 노드의 공급능력 부여하기
for i in range(len(supplies)):
    #.set_node_supply(노드번호, 공급능력)
    smcf.set_node_supply(i,supplies[i])
#최소 Cost flow 찾기
status=smcf.solve()
if status==smcf.OPTIMAL:
    print('Total cost= ', smcf.optimal_cost())
    for i in range(smcf.num_arcs()):
        #처음과 마지막 가지들 말고 가운데 흐름을 본다
        if smcf.tail(i)!=source and smcf.head(i)!=sink:
            #의사결정 변수의 값(capacity)가 0보다 클 때
            if smcf.flow(i)>0:
                print('Worker %d assigned to task %d. Cost= %d'%(smcf.tail(i),smcf.head(i),smcf.unit_cost(i)))

