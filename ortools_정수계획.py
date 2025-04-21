from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')

#예제2_BigM 활용 (Either-Or/K out of N 제약 조건이 일 때 사용 용이)
#의사결정 변수: 생산 시간
# x1:공장1-장난감1, x2:공장1-장난감2
#x3:공장2-장난감1, x4:공장2-장난감2
x={}
for i in range(4):
    x[i]=solver.NumVar(0,solver.infinity(),'x[%i]'%i)

#공장 선택 제약조건(Either-Or, 둘 중 하나 선택)
y=solver.BoolVar('y')
M=1000000
#y가 0이면 공장 1 가동, y가 1이면 공장2 가동
solver.Add(x[0]+x[1]<=M*(1-y))
solver.Add(x[2]+x[3]<=M*y)

#장난감 생산 제약조건(K out of N, 결정 변수 여러개 생성)
z={}
for i in range(2):
    z[i]=solver.BoolVar('z[%i]'%i)
solver.Add(x[0]+x[2]<=M*z[0])
solver.Add(x[1]+x[3]<=M*z[1])
#생산 시간 제약식 설정
solver.Add(x[0]+x[1]<=500)
solver.Add(x[2]+x[3]<=700)
#목적함수 설정
solver.Maximize(10*(50*x[0]+40*x[2])+15*(40*x[1]+25*x[3])-50000*z[0]-80000*z[1])

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(4):
        print(x[i].name(),':',x[i].solution_value())