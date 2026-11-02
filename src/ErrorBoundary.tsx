import { Component, ReactNode } from 'react'
/** Shows a friendly message instead of a blank white page if rendering throws. */
export default class ErrorBoundary extends Component<{ children: ReactNode }, { err: Error | null }> {
  state = { err: null as Error | null }
  static getDerivedStateFromError(err: Error) { return { err } }
  componentDidCatch(err: Error) { console.warn('[ErrorBoundary]', err) }
  render() {
    if (!this.state.err) return this.props.children
    return <div className="max-w-md mx-auto mt-24 p-8 text-center rounded-3xl bg-white shadow">
      <div className="text-5xl mb-3">😵‍💫</div>
      <h1 className="font-bold text-lg mb-2">Ối, trang gặp lỗi rồi</h1>
      <p className="text-sm text-slate-600 mb-4">Thử tải lại trang nhé. Nhật ký và mục yêu thích của bạn vẫn được lưu trên máy.</p>
      <button className="btn btn-primary" onClick={() => location.reload()}>Tải lại</button>
    </div>
  }
}
