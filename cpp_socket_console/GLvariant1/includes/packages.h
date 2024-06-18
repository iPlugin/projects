#ifndef PACKAGES_H
#define PACKAGES_H

#pragma pack(push, 1)

struct Message {
    enum class Type { INTRO, FILE, WAIT, RESULT };
    Type type;
    union type_message {

        struct ServerIntroduce {
            char intro[2044];
        } server_introduced;

        struct FileSearch {
            char filename[50];
        } file_search;

        struct Waiting {
            char plswait[30];
        } please_wait;

        struct Result {
            char result[50];
        } result_path;
    } msg;
};

static_assert(sizeof(Message) == 2048, "Message struct size is not 2048 bytes");

#pragma pack(pop)

#endif // PACKAGES_H
