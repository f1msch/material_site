import { createStore } from 'vuex'

export default createStore({
  state: {
    // 应用状态
    user: null,
    searchQuery: '',
    filters: {
      category: '',
      material_type: '',
      ordering: '-created_at'
    }
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_SEARCH_QUERY(state, query) {
      state.searchQuery = query
    },
    SET_FILTERS(state, filters) {
      state.filters = { ...state.filters, ...filters }
    }
  },
  actions: {
    updateSearchQuery({ commit }, query) {
      commit('SET_SEARCH_QUERY', query)
    },
    updateFilters({ commit }, filters) {
      commit('SET_FILTERS', filters)
    }
  },
  getters: {
    isAuthenticated: state => !!state.user,
    currentFilters: state => state.filters
  }
})