import request from '@/utils/request'

export interface Banner {
  id: string
  title: string
  subtitle: string
  image: string
  link: string
}

export interface Feature {
  id: string
  title: string
  description: string
  icon: string
}

export interface Partner {
  id: string
  name: string
  logo: string
}

export function getBanners() {
  return request({
    url: '/api/home/banners',
    method: 'get'
  })
}

export function getFeatures() {
  return request({
    url: '/api/home/features',
    method: 'get'
  })
}

export function getPartners() {
  return request({
    url: '/api/home/partners',
    method: 'get'
  })
} 