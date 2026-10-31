/* A deterministic terminal receiver for an isolated Herdr integration test.
 * This is not an LLM. Build as "codex" solely to exercise foreground checks. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <sys/wait.h>

static void report(char *session, char *pane, const char *state) {
    pid_t child = fork();
    if (child == 0) {
        freopen("/dev/null", "w", stdout);
        execlp("herdr", "herdr", "--session", session, "pane", "report-agent",
               pane, "--source", "custom:reply-canary", "--agent", "codex",
               "--state", state, "--agent-session-id", "reply-canary-native", NULL);
        _exit(1);
    }
    waitpid(child, NULL, 0);
}

int main(int argc, char **argv) {
    if (argc != 4) return 2;
    struct termios original, raw;
    if (tcgetattr(STDIN_FILENO, &original)) return 3;
    raw = original;
    cfmakeraw(&raw);
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);
    setbuf(stdout, NULL);
    report(argv[1], argv[2], "idle");
    printf("\033[2J\033[H› \033[?2004h");
    char buffer[65536], ch;
    size_t count = 0;
    while (read(STDIN_FILENO, &ch, 1) == 1) {
        if (ch == '\r') {
            FILE *f = fopen(argv[3], "a");
            if (!f) return 4;
            fwrite(buffer, 1, count, f);
            fputs("\n--SUBMITTED--\n", f);
            fclose(f);
            count = 0;
            report(argv[1], argv[2], "working");
            printf("\033[2J\033[HWorking\r\n");
            sleep(2);
            report(argv[1], argv[2], "idle");
            printf("\033[2J\033[H› ");
        } else if (count < sizeof(buffer)) buffer[count++] = ch;
    }
    tcsetattr(STDIN_FILENO, TCSANOW, &original);
    return 0;
}
