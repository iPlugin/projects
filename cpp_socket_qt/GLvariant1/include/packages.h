#ifndef PACKAGES_H
#define PACKAGES_H

#pragma pack(push, 1)

struct Message{
    enum Type {SERVER_INTRODUCED, FILE_SEARCH, PLEASE_WAIT, DURATION, RESULT};
    Type type;
    union type_message{

        struct SERVER_INTRODUCED{
            char intro[2048];
        } msg_intro;

        struct FILE_SEARCH{
            char filename[50];
        } msg_file_search;

        struct PLEASE_WAIT{
            char plswait[30];
        } msg_plswait;

        struct DURATION{
            char duration[30];
        } msg_duration;

        struct RESULT{
            char result[50];
        } msg_result;

        char padding[2048 - sizeof(Type)];
    } msg;
};

#pragma pack(pop)

#endif // PACKAGES_H
