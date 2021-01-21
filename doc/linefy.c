#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <libgen.h>
#include <ctype.h>

struct Params
{
	FILE* input_file;
	int is_singlefy_mode;
	int is_newlinefy_mode;
};

void print_usage(char* file_name)
{
	fprintf(stderr, "Usage: ./%s <-s||-n> <input_file>\n", basename(file_name));
}

FILE* safe_open(char* file_path, char* mode)
{
	FILE* fp;

	fp = fopen(file_path, mode);

	if (fp == NULL)
	{
		fprintf(stderr, "\"%s\" open error\n", file_path);
		exit(1);
	}

	return fp;
}

struct Params check_args(int argc, char** argv)
{
	struct Params params = { NULL, 0, 0 };

	if (argc != 3)
	{
		print_usage(argv[0]);
		exit(1);
	}

	params.is_singlefy_mode = !strcmp(argv[1], "-s");
	params.is_newlinefy_mode = !strcmp(argv[1], "-n");

	if (params.is_singlefy_mode == 0 && params.is_newlinefy_mode == 0)
	{
		fprintf(stderr, "\"%s\" is an invalid option\n", argv[1]);
		fprintf(stderr, "  -s to singlefy output\n");
		fprintf(stderr, "  -n to newlinefy output\n");
		exit(1);
	}

	params.input_file = safe_open(argv[2], "r");

	return params;
}

void singlefy_output(FILE* input_file)
{
	int c;
	int is_empty_line;

	is_empty_line = 1;

	while ((c = fgetc(input_file)) != EOF)
	{
		if (c == '\n')
		{
			is_empty_line ? printf("\n") : printf(" ");
			is_empty_line = 1;
			continue;
		}

		printf("%c", (char) c);
		is_empty_line = isblank(c);
	}
}

char* insert_char(char c, char* word_buffer, int word_size, int* buffer_size)
{
	int i;
	char* new_word_buffer;

	if (word_size >= *buffer_size)
	{
		*buffer_size += 10;
		new_word_buffer = malloc(*buffer_size * sizeof(char));
		for (i=0; i<word_size; i++)
			new_word_buffer[i] = word_buffer[i];
		new_word_buffer[i] = c;
		//free(word_buffer);
		return new_word_buffer;
	}

	word_buffer[word_size-1] = c;
	return word_buffer;
}

void flush(char* word_buffer, int buffer_size)
{
	for (int i=0; i<buffer_size; i++)
		word_buffer[i] = 0;
}

void newlinefy_output(FILE* input_file)
{
	int c;
	int l;
	int word_size;
	int buffer_size;
	char* word_buffer;

	l = 1;
	word_size = 0;
	buffer_size = 10;
	word_buffer = malloc(buffer_size * sizeof(char));
	word_buffer[word_size-1] = -1;

	while ((c = fgetc(input_file)) != EOF)
	{
		flush(word_buffer, buffer_size);
		while (!isblank(c) && isprint(c))
		{
			word_size++;
			insert_char(c, word_buffer, word_size, &buffer_size);
			c = fgetc(input_file);
		}

		printf("%c", c);
		l = l+1+word_size;
		word_size = 0;

		if (l >= 80)
		{
			c == '\n' ? printf(" ") : printf("\n");
			l = 1;
			continue;
		}

		printf("%s", word_buffer);
	}
}

void print_output(struct Params params)
{
	if (params.is_singlefy_mode)
	{
		singlefy_output(params.input_file);
		return;
	}

	if (params.is_newlinefy_mode)
	{
		newlinefy_output(params.input_file);
		return;
	}
}

int main(int argc, char** argv)
{
	struct Params params;

	params = check_args(argc, argv);

	print_output(params);

	return 0;
}
