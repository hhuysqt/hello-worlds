#include <stdlib.h>
#include <stdio.h>

int main(void)
{
	char *newptr;
	int i;
	for(i = 0; (newptr = (char*)malloc(1024*1024*1024)) != NULL; i++);
	perror("malloc");
	printf("Malloc'ed %d GB (0x%x).\n", i, i);
	getchar();
	return 0;
}
