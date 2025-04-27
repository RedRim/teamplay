<template>
    <div>
        <h1>Страница с постами</h1>
        <my-input
            v-model="searchQuery"
            placeholder="Поиск..."
        />
        <div class="app__btns">
            <my-button
                @click="showDialog"
            >
                Создать пост
            </my-button>
            <my-select
                v-model="selectedSort"
                :options="sortOptions"
            />
        </div>
        
        <my-dialog v-model:show="dialogVisible">
            <post-form
                @create="createPost"
            />
        </my-dialog>
        <post-list 
            :posts="sortedAndSearchPosts"
            @remove="removePost"
            v-if="!isPostsLoading"
        />
        <div v-else>Идет загрузка...</div>
        <div ref="observer" class="observer"></div>
        <!-- <div class="page__wrapper">
            <div
                v-for="pageNumber in totalPages"
                :key="pageNumber"
                class="page"
                :class="{
                    'current-page': page === pageNumber
                }"
                @click="changePage(pageNumber)"
            >
            {{ pageNumber }}
            </div> 
        </div> -->
    </div>
</template>

<script>
import PostForm from "@/components/PostForm";
import PostList from "@/components/PostList";
import { useLoginStore } from "@/stores/login";

import axios from "axios";
export default {
    components: {
        PostForm,
        PostList,
    },
    setup() {
        const tokens = JSON.parse(localStorage.getItem('userTokens'));
        return { tokens };
    },
    data() {
        return {
            posts: [],
            dialogVisible: false,
            isPostsLoading: false,
            selectedSort: '',
            searchQuery: '',
            page: 1,
            limit: 10,
            totalPages: 0, 
            sortOptions: [
                {value: 'title', name: 'По названию'},
                {value: 'body', name: 'По описанию'},
            ],
        }
    },
    methods: {
        createPost(post) {
            this.posts.push(post); 
            this.dialogVisible = false;
        },
        removePost(post) {
            this.posts = this.posts.filter(p => p.id !== post.id)
        },
        showDialog() {
            this.dialogVisible = true;
        },
        async fetchPosts() {
            try {
                this.isPostsLoading = true;
                const response = await axios.get('https://jsonplaceholder.typicode.com/posts', {
                    params: {
                        _page: this.page,
                        _limit: this.limit,
                    }
                });
                this.posts = response.data;
                this.totalPages = Math.ceil(response.headers['x-total-count'] / this.limit); 
            } catch (e) {
                alert(e.message);
            } finally {
                this.isPostsLoading = false;
            }
        },
        async loadMorePosts() {
            this.page++;
            try {
                const response = await axios.get('https://jsonplaceholder.typicode.com/posts', {
                    params: {
                        _page: this.page,
                        _limit: this.limit,
                    }
                });
                this.posts = [...this.posts, ...response.data];
                this.totalPages = Math.ceil(response.headers['x-total-count'] / this.limit); 
            } catch (e) {
                alert(e.message);
            }
        },
        // changePage(pageNumber) {
        //     this.page = pageNumber; 
        // }
    },
    mounted() {
        this.fetchPosts();
        console.log(this.$refs.observer);
        const options = {
            rootMargin: "0px ",
            threshold: 1.0,
        };
        const callback = (entries, observer) => {
            if (entries[0].isIntersecting && this.page < this.totalPages) {
                  this.loadMorePosts();
            }
        };
        const observer = new IntersectionObserver(callback, options);
        observer.observe(this.$refs.observer);

    },
    computed: {
        sortedPosts() {
            return [...this.posts].sort((post1, post2) => {
                return post1[this.selectedSort]?.localeCompare(post2[this.selectedSort])
            })
        },
        sortedAndSearchPosts() {
            return this.sortedPosts.filter(post => post.title.toLowerCase().includes(this.searchQuery.toLowerCase() )) 
        }
    },
    watch: {
        // page() {
        //     this.fetchPosts();
        // }
    }
}
</script> 

<style scoped>
.app__btns {
    margin: 15px 0;
    display: flex;
    justify-content: space-between;
}

.page__wrapper {
    display: flex;
    margin-top: 15px;;
}   

.page {
    border: 1px solid black;
    padding: 10px;
}

.current-page {
    border: 2px solid teal;
}

.observer {
    height: 30px;
    background: skyblue;
}
</style>