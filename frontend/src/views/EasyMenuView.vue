<template>
    <div>
        <phone-header></phone-header>
        <div v-if="modalStatus === true" class="overlay_modal">
            <img
                @click="
                    () => {
                        modalStatus = false;
                    }
                "
                src="../assets/app-icon/add-alert.svg"
            />
        </div>
        <!-- 최초 로그인 시 브3 승급, MMF 추천 모달 -->
        <div v-if="bronze" class="overlay_modal">
            <img
                @click="
                    () => {
                        this.$store.state.total_apps[3].added = true;
                        bronze = false;
                    }
                "
                src="../assets/app-icon/add-menu-modal.svg"
            />
        </div>
        <div class="easy-menu-header">
            <span v-if="isLogin === null" style="font-size: 14px; color: white">만나서 반가워요!</span>
            <span v-else style="font-size: 14px; color: white"
                ><img @click="moveToTierMain" style="width: 32px" :src="userDetail.tier ? tier[userDetail.tier].img : null" /> {{ userDetail.name }}님</span
            >
            <div class="edit-box">
                <img @click="toggleEdit" v-if="changeMode === false" class="icon" src="../assets/top/edit-icon.png" />
                <img @click="toggleEditFin" v-else-if="changeMode === true" class="icon" src="../assets/top/edit-fin-icon.png" />
                <img class="icon" src="../assets/top/bell-icon.png" />
                <router-link to="/menu_setting"><img class="icon" src="../assets/top/setting-icon.png" /></router-link>
            </div>
        </div>
        <div v-if="isLogin" class="my-asset">
            <p style="font-size: 16px; font-weight: 500; margin-bottom: 5px">총 자산</p>
            <p style="font-size: 24px; font-weight: 600">0원</p>
            <p style="color: red; font-size: 12px">+0원 (0.0%)</p>
        </div>
        <div style="display: flex; justify-content: space-around; margin-top: 30px" v-else>
            <div class="app my-grid-item" v-for="item in defaultLayout" :key="item">
                <img :src="item.img" />
                {{ item.name }}
            </div>
        </div>
        <div id="my-apps" v-if="isLogin">
            <my-grid-layout
                :col-num="12"
                :row-height="30"
                :is-draggable="changeMode ? draggable : false"
                :is-resizable="false"
                :is-mirrored="false"
                :responsive="responsive"
                :vertical-compact="true"
                :margin="[10, 10]"
                :use-css-transforms="true"
                :layout="layout"
            >
                <my-grid-item
                    style="text-align: center; display: flex; flex-direction: column; justify-content: space-between; align-items: center"
                    v-for="(item, index) in layout"
                    :x="item.x"
                    :y="item.y"
                    :w="item.w"
                    :h="item.h"
                    :i="item.i"
                    :key="item.i"
                >
                    <img
                        v-if="item.added === true && changeMode === true"
                        @click="removeItem(item.i)"
                        class="remove"
                        style="width: 18px; height: 18px"
                        src="../assets/top/minus-cirlce.png"
                    />
                    <img @click="movePage(index)" v-if="item.added === true" :src="item.img" :style="{ opacity: imgOpacity }" />
                    <div v-if="item.added === true" style="font-size: 10px">{{ item.name }}</div>
                    <img
                        v-if="item.added === false && changeMode === true"
                        @click="addItem(item.i)"
                        class="remove"
                        style="width: 18px; height: 18px"
                        src="../assets/top/add-circle.svg"
                    />
                    <img v-if="item.added === false && changeMode === true" :src="item.img" :style="{ opacity: addImgOpacity }" />
                    <div v-if="item.added === false && changeMode === true" style="font-size: 10px">{{ item.name }}</div>
                </my-grid-item>
            </my-grid-layout>
        </div>
    </div>

    <div style="position: absolute; bottom: 30px; left: 18.5px" v-if="isLogin === null">
        <router-link to="/login"><div class="login-btn">로그인</div></router-link>
        <router-link to="/make_account"><div class="make-account-btn">계좌만들기</div></router-link>
    </div>
</template>

<script>
import PhoneHeader from "@/components/PhoneHeader.vue";
import { GridLayout, GridItem } from "vue3-grid-layout-next";
export default {
    data() {
        return {
            modalStatus: false,
            changeMode: false,
            defaultLayout: [
                { x: 0, y: 0, w: 4, h: 2.5, i: "0", name: "이체", img: require("../assets/app-icon/이체.svg"), static: true },
                { x: 4, y: 0, w: 4, h: 2.5, i: "1", name: "내 계좌 확인", img: require("../assets/app-icon/계좌확인.svg"), static: true },
                { x: 8, y: 0, w: 4, h: 2.5, i: "2", name: "고객센터", img: require("../assets/app-icon/고객센터.svg"), static: true },
            ],
            draggable: true,
            resizable: true,
            index: 3,
            isB3TierUp: false,
            isB2TierUp: false,
            bronze: false,
        };
    },
    components: {
        PhoneHeader,
        myGridLayout: GridLayout,
        myGridItem: GridItem,
    },
    computed: {
        userDetail() {
            return this.$store.state.userDetail;
        },
        isLogin() {
            return sessionStorage.getItem("accessToken");
        },
        imgOpacity() {
            return this.changeMode ? 0.5 : 1;
        },
        addImgOpacity() {
            return this.changeMode ? 1 : 0.5;
        },
        layout() {
            return this.$store.state.total_apps;
        },
        tier() {
            return this.$store.state.checkTier;
        },
    },
    methods: {
        toggleEdit() {
            if (this.isLogin === null) {
                alert("로그인이 필요합니다.");
                this.$router.push("/login");
                return;
            }
            if (this.modalStatus === false) {
                this.modalStatus = true;
            }
            console.log(this.$store.state.total_apps);
            this.layout.forEach((item) => {
                item.static = !item.static;
            });
            this.changeMode = !this.changeMode;
        },
        toggleEditFin() {
            console.log(this.$store.state.total_apps);
            this.layout.forEach((item) => {
                item.static = !item.static;
            });
            this.changeMode = !this.changeMode;
        },
        addItem: function (index) {
            this.$store.state.total_apps[index].added = true;
        },
        removeItem: function (index) {
            this.$store.state.total_apps[index].added = false;
        },
        moveToTierMain() {
            this.$router.push("/tier_main");
        },
        movePage(index) {
            if (index === 0) {
                this.$router.push("/send_money");
            } else if (index === 1) {
                this.$router.push("/check_account");
            } else if (index === 5) {
                this.$router.push("/buy_stock");
            }
        },
    },

    created() {
        this.$store.dispatch("GET_USER_DETAIL").then((res) => {
            if (sessionStorage.getItem("tier") != "undefined" && this.$store.state.userDetail.tier !== sessionStorage.getItem("tier")) {
                this.isB2TierUp = true;
            }
        });
    },
    mounted() {
        console.log(this.userDetail);
        if (sessionStorage.getItem("accessToken")) {
            console.log(sessionStorage.getItem("B3Flag"));
            if (!sessionStorage.getItem("B3Flag") || sessionStorage.getItem("B3Flag") == "false") {
                this.bronze = true;
                sessionStorage.setItem("B3Flag", true);
            }
        }
    },
};
</script>

<style>
.my-grid-item {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

.remove {
    cursor: pointer;
    position: absolute;
    right: 2px;
}
.login {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    margin-left: 10px;
    margin-top: 20px;
}
.app {
    font-size: 10px;
    width: 93px;
    height: 90px;
    margin-bottom: 10px;
}
.easy-menu-header {
    width: 291px;
    height: 46px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #354ef2;
    margin: 0 auto;
    margin-top: 51px;
    padding: 0 12px;
    border-radius: 6px;
}

.edit-box {
    display: flex;
    align-items: center;
}

.icon {
    margin-left: 10px;
    width: 24px;
    height: 24px;
}

.my-asset {
    width: 291px;
    height: 95px;
    background-color: #f0f0f0;
    border-radius: 6px;
    text-align: left;
    margin: 0 auto;
    margin-top: 11px;
    padding-left: 12px;
    padding-top: 4px;
    box-sizing: border-box;
}

.groups {
    display: flex;
    justify-content: stretch;
}

.group {
    flex: 1;
}

/* #my-apps {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
} */

.drag-item {
    width: 105px;
    height: 105px;
    border: 1px solid black;
}

.login-btn {
    background-color: #354ef2;
    color: white;
    border-radius: 25px;
    width: 283px;
    height: 50px;
    margin: 0 auto;
    line-height: 50px;
    margin-top: 60px;
    font-weight: 700;
}

.make-account-btn {
    background-color: #a8b4ff;
    color: #354ef2;
    border-radius: 25px;
    width: 283px;
    height: 50px;
    margin: 0 auto;
    line-height: 50px;
    margin-top: 20px;
    font-weight: 700;
}

.vue-grid-layout {
    background: #ffffff;
}
.vue-grid-item:not(.vue-grid-placeholder) {
    background: #ffffff;
}
.vue-grid-item .resizing {
    opacity: 0.9;
}
.vue-grid-item .static {
    background: rgb(255, 255, 255);
}
.vue-grid-item .text {
    font-size: 10px;
    text-align: center;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    height: 100%;
    width: 100%;
}
.vue-grid-item .no-drag {
    height: 100%;
    width: 100%;
}
.vue-grid-item .minMax {
    font-size: 12px;
}
.vue-grid-item .add {
    cursor: pointer;
}
.vue-draggable-handle {
    position: absolute;
    width: 20px;
    height: 20px;
    top: 0;
    left: 0;
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='5' fill='#999999'/></svg>") no-repeat;
    background-position: bottom right;
    padding: 0 8px 8px 0;
    background-repeat: no-repeat;
    background-origin: content-box;
    box-sizing: border-box;
    cursor: pointer;
}

.overlay_modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 5;
}
</style>
