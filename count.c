#include <stdio.h>

int main(void)
{
	int a[] = { 3, 18, 1, 7, 8, 9, 11, 13, 20, 1, 4, 7, 8, 9, 10, 20, 17,
		20, 3, 20, 7, 13, 11, 13, 20, 16, 7, 9, 10, 17, 8, 9, 5, 6 };
	
	int cnt[20] = { 0 };
	int size, i, j;

	size = sizeof(a) / sizeof(a[0]);
	for (i = 0; i < size; i++)
		cnt[a[i] - 1]++;

	for (i = 0; i < 20; i++)
		printf("%d: %d°³\n", i + 1, cnt[i]);

	return 0;
}
