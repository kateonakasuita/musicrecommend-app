import os
import streamlit as st

# 1. ページの基本設定
st.set_page_config(page_title="MIDI 楽曲スタイル変換デモ", page_icon="🎵")

# 2. タイトルと説明文
st.title("🎵 MIDI 楽曲スタイル変換")
st.write(
    "曲とスタイル（または気分）を選択すると、アレンジ音源を試聴・ダウンロードできます。"
)

st.divider()

# 3. 楽曲の選択
st.subheader("1. 変換したい曲を選択")
song = st.selectbox(
    "曲を選んでください",
    ["夜に駆ける", "ドライフラワー", "水平線"],
)

# フォルダ名と元のMIDIファイル名のマッピング
song_info = {
    "夜に駆ける": {"folder": "yorunikakeru", "file": "yorunikakeru.mid"},
    "ドライフラワー": {"folder": "doraiflower", "file": "doraiflower.mid"},
    "水平線": {"folder": "suiheisen", "file": "suiheisen.mid"},
}

selected_folder = song_info[song]["folder"]
selected_file = song_info[song]["file"]

st.divider()

# 4. 原曲の試聴・確認エリア
st.subheader("2. 原曲（オリジナル）")
orig_mp3_path = f"audio/{selected_folder}/original.mp3"
orig_mid_path = f"audio/{selected_folder}/{selected_file}"

if os.path.exists(orig_mp3_path):
    st.audio(orig_mp3_path)
elif os.path.exists(orig_mid_path):
    st.success(f"🎵 原曲MIDIファイルを発見: `{selected_file}`")
    st.info("💡 音声再生用（.mp3）に変換するか配置するとここで聴けるようになります。")
else:
    st.info(f"💡 `audio/{selected_folder}/{selected_file}` を配置すると原曲を認識します。")

st.divider()

# 5. スタイル選択ボタン
st.subheader("3. どんなスタイルがいい？")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎹 ピアノ風", use_container_width=True):
        st.session_state["style"] = "piano"
        st.session_state["reason"] = "🎹 ピアノ風"

with col2:
    if st.button("🎷 ジャズ風", use_container_width=True):
        st.session_state["style"] = "jazz"
        st.session_state["reason"] = "🎷 ジャズ風"

with col3:
    if st.button("🎶 オルゴール風", use_container_width=True):
        st.session_state["style"] = "musicbox"
        st.session_state["reason"] = "🎶 オルゴール風"

# 6. 気分選択ボタン
st.subheader("4. あなたの気分は？")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("楽しい 😀", use_container_width=True):
        st.session_state["style"] = "piano"
        st.session_state["reason"] = "楽しい 😀（ピアノ風）"

with col2:
    if st.button("チル 😎", use_container_width=True):
        st.session_state["style"] = "jazz"
        st.session_state["reason"] = "チル 😎（ジャズ風）"

with col3:
    if st.button("落ち着きたい 😆", use_container_width=True):
        st.session_state["style"] = "musicbox"
        st.session_state["reason"] = "落ち着きたい 😆（オルゴール風）"

# 7. 再生・ダウンロードエリア
if "style" in st.session_state:
    selected_style = st.session_state["style"]
    reason = st.session_state.get("reason", "")
    st.write("---")

    file_path = f"audio/{selected_folder}/{selected_style}.mp3"

    st.success(f"**「{song}」** の **「{reason}」** を選択中")

    if os.path.exists(file_path):
        st.audio(file_path)

        with open(file_path, "rb") as f:
            st.download_button(
                label=f"📥 {song}（{selected_style}）の音源をダウンロード",
                data=f,
                file_name=f"{selected_folder}_{selected_style}.mp3",
                mime="audio/mp3",
            )
    else:
        st.warning(
            f"⚠️ 音声ファイル `{file_path}` がまだありません。`audio/{selected_folder}/` フォルダに入れてください。"
        )
