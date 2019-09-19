<template>
	<div class="layout">
		<Layout>
			<Header :style="{position: 'fixed', width: '100%'}" style="z-index: 999">
<!--				<Dropdown trigger="custom" :visible="suggest.length!=0">-->
				<div class="search" >
						<Input search enter-button="Search" placeholder="请输入搜索的内容"
									v-model="input" :maxlength=50 autofocus style="width: 80%;margin: 0 auto"
									@on-search="searchBtn" @on-change="suggestBtn"/>
					</div>
<!--					<DropdownMenu slot="list">-->
<!--						<DropdownItem v-for="(i,index) in suggest" :key="index">{{i}}</DropdownItem>-->
<!--					</DropdownMenu>-->
				<div class="search-select">
					<transition-group name="itemfade" tag="ul" mode="out-in" v-cloak>
						<li v-for="(value,index) in suggest" :class="{selectback:index==now}"
								class="search-select-option search-select-list" @mouseover="selectHover(index)"
								@click="selectClick(index)" :key="value">
							{{value}}
						</li>
					</transition-group>
				</div>
<!--				</Dropdown>-->
			</Header>
			<Content :style="{margin: '88px 20px 0', background: '#fff', minHeight: '500px'}">
					<div v-show="total||flag" class="search_tool">
						<i class="c-icon searchTool-spanner c-icon-setting">
							<span class="nums_text">相关结果约{{total}}个</span>
							<br>
							<span class="nums_text">当前页面结果共{{result.length}}个</span>
						</i>
					</div>
				<div>
						<Tabs v-show="flag" type="card" size="small" style="margin: 0 80px;" @on-click="tabChange">
							<TabPane label="全部" 	name="0"></TabPane>
							<TabPane label="最新电影" 	name="1"></TabPane>
							<TabPane label="国内电影" 	name="2"></TabPane>
							<TabPane label="欧美电影" 	name="3"></TabPane>
							<TabPane label="旧版综艺" 	name="4"></TabPane>
							<TabPane label="游戏下载" 	name="5"></TabPane>
							<TabPane label="其它电影" 	name="6"></TabPane>
							<TabPane label="欧美电视" 	name="7"></TabPane>
							<TabPane label="最新综艺" 	name="8"></TabPane>
							<TabPane label="华语电视" 	name="9"></TabPane>
							<TabPane label="动漫资源" 	name="10"></TabPane>
						</Tabs>
					<ul  class="content-ul" v-for="i in result" :key="i.id">
							<li class="content-li" >
								<div class="container">
									<div class="left" >
										<img class="left" :src="i.movie_img?i.movie_img:default_img" @error="defImgError" >
										<Button icon="ios-download-outline"
														type="primary"
														size="small"
														v-clipboard:copy="i.movie_url"
														v-clipboard:success="onCopy"
														v-clipboard:error="onError">
											复制链接</Button>
									</div>
									<div class="right" >
										<h2>
											<a :href="`https://www.dytt8.net/${i.page_url}`" target="_blank" v-html="i.name">
											</a>
										</h2>
										<p>
											类型:<span>{{i.type}}</span>
										</p>
										<p>
											年份:<span>{{i.year}}</span>
										</p>
										<p>
											简介:<span v-html="i.movie_desc"></span>
										</p>
									</div>
								</div>
							</li>
						</ul>
					<div v-if="!result.length&&flag" class="content-ul" style="position: relative;left: 20%">
						<img src="https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=30305038,711507037&fm=26&gp=0.jpg">
					</div>
				</div>
				<Page class="page" v-if="total" :total="total" :page-size="Number(page_limit)" @on-change="onChange"
							show-sizer @on-page-size-change="pageChange"/>
			</Content>
			<Footer class="layout-footer-center">2019-2025 &copy; TalkingData</Footer>
		</Layout>
	</div>
</template>

<script>
	import {search,suggest} from '../api/index'

  export default {
    name: "index",
		data(){
      return {
        input:'',		//用户输入的搜索内容
				type:0,			//用户选择的分类
        page_office:0,					//游标
        page_limit:10,					//每页数量
				flag:false,							//是否展示tab栏目

				inputSize:'width: 60%;',		//搜索框尺寸
				result:[],						//搜索结果
				suggest:[],						//搜索建议
				now:null,							//用户当前停留的搜索建议下标
				total:undefined,				//搜索结果总数
				default_img:"https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3885376987,415548851&fm=111&gp=0.jpg",		//默认图
        logo: 'this.src="' + this.default_img + '"'  ,
      }
		},
		methods:{
      async suggestBtn(){
        if (!this.input.trim()) {
          this.suggest=[]
          return null
				}
        let params={
          q:this.input,
					size:5,
				}
        let res=await suggest(params)
				if(res.data.success){
					this.suggest=res.data.data
				}
			},
      async searchBtn(){
        if(!this.input.trim()){
          return this.$Notice.error({
            title:'未输入搜索内容!',
            duration:1.5,
          })
        }
        let params={
          q:this.input,
					type:this.type,
					offset:this.page_offset,
					limit: this.page_limit
				}
        let res=await search(params)
				if(res.data.success){
					this.result=res.data.data.hits
					this.total=res.data.data.total
					this.flag=true
				}
        this._clearSuggest()
        document.documentElement.scrollTop=0
			},
      // 迅雷复制到剪贴板
			onCopy () {
        this.$Message.success({
          content: `复制成功,请直接打开迅雷!`,
					duration:1.5
        });
      },
      onError () {
        return this.$Message.error({
          content:'出现错误,请重试!',
          duration:1.5,
        })
      },
			// 切换页面
			onChange(page) {
        this.page_offset = (page-1) * this.page_limit
				this.searchBtn()
      },
			// 分类切换
			tabChange(name){
        if(!this.input.trim()) {
          this.flag=false
					this.result=[]
					this.total=0
          return this.$Notice.error({
            title: '未输入搜索内容!',
            duration: 1.5,
          })
        }
        this.page_offset=0
				this.page_limit=10
				this.type=name
			},
			// 背景图片加载失败时
			defImgError(event){
        event.target.src = this.default_img;
			},
			// 翻页时
			pageChange(page){
        this.page_limit=page
				this.searchBtn()
			},
			// 鼠标移动到搜索建议时
      selectHover(index) {
        this.now = index
      },
			// 鼠标点击搜索建议时
      selectClick(index) {
        this.input = this.suggest[index];
        this.searchBtn();
      },
			_clearSuggest(){
        this.suggest=[]
			}
		},
		watch:{
      type(){
        this.searchBtn()
			}
		}
  }
</script>

<style scoped lang="scss">
	.layout{
		border: 1px solid #d7dde4;
		background: #f5f7f9;
		position: relative;
		border-radius: 4px;
		overflow: hidden;
	}
	.layout-logo{
		width: 100px;
		height: 30px;
		background: #5b6270;
		border-radius: 3px;
		float: left;
		position: relative;
		top: 15px;
		left: 20px;
	}
	.layout-nav{
		width: 420px;
		margin: 0 auto;
		margin-right: 20px;
	}
	.layout-footer-center{
		text-align: center;
	}
	.search{
		position: relative;
		top: 25%;
	}
	.nums_text{
		line-height: 42px;
		font-size: 12px;
		color: #999;
	}
	.container{
		overflow: hidden;
	}
	.left{
		float: left;
		width: 100px;
		padding-bottom: 10000px;
		margin-bottom: -10000px;
	}
	.right{
		padding-left: 15px;
		max-height: 180px;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 7;
		overflow: hidden;
	}
	.content-ul {
		padding: 20px 80px;
		.content-li{
			padding-bottom: 20px;
		}
	}
	.page{
		margin: 0 auto;
		width: 460px;
	}
	.ivu-dropdown {
		padding: 25px;
	}


	.search-select li {
		border: 1px solid #d4d4d4;
		line-height: 1.2!important;
		border-top: none;
		border-bottom: none;
		background-color: #fff;
		width: 100%;
	}
	.search-select li:last-child{
		border-bottom-left-radius:20px;
		border-bottom-right-radius:20px;
	}
	.search-select ul:last-child{
		background-color: #7e8c8d;
		border-bottom-left-radius:20px;
		border-bottom-right-radius:20px;
	}

	.search-select-option {
		box-sizing: border-box;
		padding: 7px 10px;
	}
	.selectback {
		background-color: #eee !important;
		cursor: pointer
	}
	.search-select-list {
		transition: all 0.5s
	}
	.itemfade-enter,
	.itemfade-leave-active {
		opacity: 0;
	}
	.itemfade-leave-active {
		position: absolute;
	}
	.selectback {
		background-color: #eee !important;
		cursor: pointer
	}
	.search-select {
		position: relative;
		top: 25%;
		margin: 0 auto;
		box-sizing: border-box;
		width: 80%;

	}
	.search-select ul{
		margin:0;
		text-align: left;
		margin-right: 71px;
		}
</style>
