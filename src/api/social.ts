                                                                                                                                                                                                                                                                                                                       import request from '@/utils/request'

// 动态广场相关接口
export interface Post {
  id: number
  user_id: number
  user?: {
    id: number
    username: string
    nickname: string
    avatar?: string
  }
  post_type: 'text' | 'image' | 'video' | 'dance' | 'heritage'
  content: string
  media_url?: string
  likes_count: number
  comments_count: number
  shares_count: number
  is_public: boolean
  is_featured: boolean
  created_at: string
  updated_at: string
}

export interface PostCreate {
  post_type: 'text' | 'image' | 'video' | 'dance' | 'heritage'
  content: string
  media_url?: string
  is_public?: boolean
}

export interface PostComment {
  id: number
  post_id: number
  user_id: number
  user?: {
    id: number
    username: string
    nickname: string
    avatar?: string
  }
  content: string
  parent_id?: number
  created_at: string
}

export interface CommentCreate {
  content: string
  parent_id?: number
}

// 非遗传承相关接口
export interface HeritageProject {
  id: number
  name: string
  category: string
  level: 'national' | 'provincial' | 'municipal' | 'county'
  description: string
  history: string
  techniques: string
  current_status: string
  protection_measures: string
  image_url?: string
  video_url?: string
  status: 'active' | 'inactive'
  created_at: string
  updated_at: string
}

export interface HeritageInheritor {
  id: number
  name: string
  gender: 'male' | 'female'
  birth_year: number
  hometown: string
  bio: string
  achievements: string
  inheritance_years: number
  teaching_experience: string
  representative_works: string
  contact_info: string
  avatar_url?: string
  status: 'active' | 'inactive'
  created_at: string
  updated_at: string
}

// 动态广场API
export const postApi = {
  // 获取动态列表
  getPosts: (params: {
    page?: number
    page_size?: number
    post_type?: string
    user_role?: string
    is_public?: boolean
    is_featured?: boolean
  }) => {
    return request.get('/api/v1/social/posts', { params })
  },

  // 创建动态
  createPost: (data: PostCreate) => {
    return request.post('/api/v1/social/posts', data)
  },

  // 获取动态详情
  getPost: (id: number) => {
    return request.get(`/api/v1/social/posts/${id}`)
  },

  // 点赞动态
  likePost: (id: number) => {
    return request.post(`/api/v1/social/posts/${id}/like`)
  },

  // 取消点赞
  unlikePost: (id: number) => {
    return request.delete(`/api/v1/social/posts/${id}/like`)
  },

  // 获取动态评论
  getComments: (postId: number, params?: {
    page?: number
    page_size?: number
  }) => {
    return request.get(`/api/v1/social/posts/${postId}/comments`, { params })
  },

  // 添加评论
  addComment: (postId: number, data: CommentCreate) => {
    return request.post(`/api/v1/social/posts/${postId}/comments`, data)
  },

  // 删除评论
  deleteComment: (postId: number, commentId: number) => {
    return request.delete(`/api/v1/social/posts/${postId}/comments/${commentId}`)
  },

  // 切换动态精选状态（管理员）
  toggleFeatured: (id: number) => {
    return request.patch(`/api/v1/social/posts/${id}/featured`)
  },

  // 切换动态可见性（管理员）
  toggleVisibility: (id: number) => {
    return request.patch(`/api/v1/social/posts/${id}/visibility`)
  },

  // 删除动态（管理员）
  deletePost: (id: number) => {
    return request.delete(`/api/v1/social/posts/${id}`)
  }
}

// 非遗项目API
export const heritageProjectApi = {
  // 获取项目列表
  getProjects: (params: {
    page?: number
    page_size?: number
    keyword?: string
    category?: string
    level?: string
    status?: string
  }) => {
    return request.get('/api/v1/social/heritage/projects', { params })
  },

  // 创建项目
  createProject: (data: Partial<HeritageProject>) => {
    return request.post('/api/v1/social/heritage/projects', data)
  },

  // 获取项目详情
  getProject: (id: number) => {
    return request.get(`/api/v1/social/heritage/projects/${id}`)
  },

  // 更新项目
  updateProject: (id: number, data: Partial<HeritageProject>) => {
    return request.put(`/api/v1/social/heritage/projects/${id}`, data)
  },

  // 切换项目状态
  toggleStatus: (id: number) => {
    return request.patch(`/api/v1/social/heritage/projects/${id}/status`)
  },

  // 删除项目
  deleteProject: (id: number) => {
    return request.delete(`/api/v1/social/heritage/projects/${id}`)
  }
}

// 非遗传承人API
export const heritageInheritorApi = {
  // 获取传承人列表
  getInheritors: (params: {
    page?: number
    page_size?: number
    keyword?: string
    hometown?: string
    gender?: string
    status?: string
  }) => {
    return request.get('/api/v1/social/heritage/inheritors', { params })
  },

  // 创建传承人
  createInheritor: (data: Partial<HeritageInheritor>) => {
    return request.post('/api/v1/social/heritage/inheritors', data)
  },

  // 获取传承人详情
  getInheritor: (id: number) => {
    return request.get(`/api/v1/social/heritage/inheritors/${id}`)
  },

  // 更新传承人
  updateInheritor: (id: number, data: Partial<HeritageInheritor>) => {
    return request.put(`/api/v1/social/heritage/inheritors/${id}`, data)
  },

  // 切换传承人状态
  toggleStatus: (id: number) => {
    return request.patch(`/api/v1/social/heritage/inheritors/${id}/status`)
  },

  // 删除传承人
  deleteInheritor: (id: number) => {
    return request.delete(`/api/v1/social/heritage/inheritors/${id}`)
  }
} 