#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
void	signal_handle(int sig) {
	if (sig == SIGINT) {
		write(1, "\n", 1);
		return ;
	}
}

int		main() {
	int 		i;
	char 		buf[51];
	int			process;
	char 		*argv[] = {NULL, NULL};
	signal(SIGINT, signal_handle);
	while (1){
		printf("minishell -> ");
		if(fgets(buf, sizeof(buf), stdin)) {
#if TEST
			printf("%s\n", buf);
#endif
			for(i = 0; i < sizeof(buf) && buf[i]; i++)
				if(buf[i] == '\n') {
					buf[i] = '\0';
					argv[0] = buf;
					break;
				}
			process = fork();
			if (process == -1) {
				perror("fork");
				exit(1);
			}
			if (process == 0) {
				execvp(argv[0], argv);
				perror(buf);
				exit(1);
			}
			wait(NULL);
		}
		sleep(1);
	}
	return 0;
}
