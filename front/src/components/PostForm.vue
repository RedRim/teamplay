<template>
    <form @submit.prevent>
        <h4>Создание поста</h4>
        <my-input 
            v-model="post.title"
            placeholder="Введите название поста"
            style="margin-top: 15px;"
        />
        <my-input 
            v-model="post.body"
            placeholder="Введите описание поста"
            style="margin-top: 15px;" 
        />
        <my-button 
            style="align-self: flex-end; margin-top: 15px;"
            @click="createPost"
        >
            Создать пост
        </my-button>
    </form> 
</template>

<script>
export default {
    data() {
        return {
            post: {
                title: '',
                body: '',
            }
        }
    },
    methods: {
        createPost() {
            this.post.id = Date.now();
            this.$emit('create', this.post)
            this.post = {
                title: '',
                body: '',
            }
        }
    }
}
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
}
</style>