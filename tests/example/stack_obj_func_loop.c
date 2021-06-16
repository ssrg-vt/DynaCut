#include <stdio.h>
#include <unistd.h>
#include <string.h>

int func(int arg1, char *arg2)
{
	printf("     %s: arg1: 0x%x (%p), arg2: %s (%p)\n", __func__,
	       arg1, &arg1, arg2, &arg2);
	return 0;
}

int main()
{
	long i = 0;
	unsigned int obj1 = 0x123;
	unsigned long obj2 = 0x456;
	unsigned int obj3 = 0x789;
	char str[12];

	printf("pid: %d\n", getpid());
	strcpy(str, "Hello world");
	while (i < 20) {
		printf("[%02ld] %s: 0x%x 0x%lx 0x%x: %p, %p, %p. %s: %p\n",
		       ++i, __func__, obj1, obj2, obj3, &obj1, &obj2, &obj3,
		       str, &str);
		func(obj1, str);
		sleep(5);
	}
	return 0;
}
