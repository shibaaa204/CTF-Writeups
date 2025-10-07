#include <stdio.h>
#include <stdlib.h>

int main() {
    char hexstr[20];
    unsigned int hex_value;
    int signed_value;

    printf("Enter hex string (e.g. BEE0FDE9 or 0xBEE0FDE9): ");
    scanf("%s", hexstr);

    hex_value = (unsigned int)strtoul(hexstr, NULL, 16);  // base 16
    signed_value = (int)hex_value;

    printf("As unsigned int: %u\n", hex_value);
    printf("As signed int: %d\n", signed_value);
    return 0;
}
