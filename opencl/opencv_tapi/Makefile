all: test_cpu test_gpu
	@echo 'On CPU'
	@echo `time ./test_cpu`
	@echo 'On GPU'
	@echo `time ./test_gpu`

test_cpu: test_cpu.cpp 
	g++ -o test_cpu test_cpu.cpp `pkg-config --cflags --libs opencv`
test_gpu: test_gpu.cpp
	g++ -o test_gpu test_gpu.cpp `pkg-config --cflags --libs opencv`

test:
	time ls
