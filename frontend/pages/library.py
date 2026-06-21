import streamlit as st
from frontend.services.library import fetch_documents,delete_document
import os

def render_library():
    st.markdown("## 📂 Document Library")
    token = st.session_state.get("token")
    if not token:
        st.warning("Please login again.")
        return
    search_q = st.text_input("🔍 Filter documents…", placeholder="Type to search…")
    st.markdown("<br>", unsafe_allow_html=True)
    docs = fetch_documents(token)
    print("DOCUMENTS", docs)
    if not docs:
        docs = []
    if search_q:
        docs = [d for d in docs if search_q.lower() in d["filename"].lower()]
    if not docs:
        st.markdown(
            '''
            <div class="info-alert">
            ℹ️ No documents match your search.
            </div>
            ''',unsafe_allow_html=True)
        return
    for i, doc in enumerate(docs):
        c1, c2, c3, c4 = st.columns([3, 1.2, 1, 0.8])
        source_type = doc.get("source_type","unknown")
        badge_map = {
            "pdf": "📄 PDF",
            "video": "🎬 VIDEO",
            "research": "📚 RESEARCH"
        }
        icon_map = {
            "pdf": "📄",
            "video": "🎬",
            "research": "📚"
        }
        source_badge = badge_map.get(
            source_type,
            "📁 UNKNOWN"
        )
        icon = icon_map.get(
            source_type,
            "📁"
        )
        status = doc.get(
            "indexed_status",
            "unknown"
        )
        status_map = {
            "indexed": "🟢 Indexed",
            "processing": "🟡 Processing",
            "failed": "🔴 Failed"
        }
        status_label = status_map.get(status,status)
        with c1:
            st.markdown(f"**{icon} {doc['filename']}**")
            st.caption(source_badge)
            st.caption(status_label)
            # st.markdown(f"""
            #     <div style="
            #         display:flex;
            #         align-items:center;
            #         gap:.6rem;
            #         padding:.5rem 0;
            #     ">
            #         <span style="font-size:1.3rem">
            #             {icon}
            #         </span>

            #         <div style="flex:1">

            #             <div class="doc-name">
            #                 {doc['filename']}
            #             </div>

            #             <div style="
            #                 font-size:.75rem;
            #                 color:gray;
            #                 margin-top:.2rem;
            #             ">
            #                 {source_badge}
            #             </div>

            #             <div style="
            #                 font-size:.75rem;
            #                 color:gray;
            #                 margin-top:.2rem;
            #             ">
            #                 {status_label}
            #             </div>

            #         </div>
            #     </div>
            #     """,unsafe_allow_html=True)
        with c2:
            if (doc.get("filepath") and os.path.exists(doc["filepath"])):
                mime_map = {
                    "pdf": "application/pdf",
                    "video": "video/mp4",
                    "research": "application/pdf"
                }
                mime_type = mime_map.get(
                    source_type,
                    "application/octet-stream"
                )
                with open(
                    doc["filepath"],
                    "rb"
                ) as file:
                    st.download_button(
                        label="⬇ Download",
                        data=file,
                        file_name=doc["filename"],
                        mime=mime_type,
                        key=f"download_{i}"
                    )
            else:
                st.button(
                    "Unavailable",
                    disabled=True,
                    key=f"disabled_{i}"
                )
        with c3:
            if st.button("💬 Chat",key=f"chat_{i}"):
                st.session_state.selected_doc = {
                    "id": doc["id"],
                    "filename": doc["filename"],
                    "source_type": source_type
                }
                st.session_state.page = ("Chat (Q&A)")
                st.rerun()
        with c4:
            if st.button("🗑",key=f"del_{i}"):
                data, status_code = delete_document(doc["id"], token)
                if status_code == 200:
                    st.success("Document deleted successfully")
                    st.rerun()
                else:
                    st.error(
                        data.get("detail", "Failed to delete document"))
        st.divider()