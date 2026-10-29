import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="مستعرض البيانات الذكي", page_icon="🔍", layout="wide")
st.title("🔍 تطبيق استعراض البيانات حسب الأعمدة")
st.write("قم برفع أي ملف إكسل، وسيقوم التطبيق بقراءة الأعمدة وتصفية البيانات بناءً عليها تلقائياً.")

# زر رفع ملف الإكسل
uploaded_file = st.file_uploader("اختر ملف الإكسل (Excel)", type=["xlsx", "xls"])

if uploaded_file is not None:
    # قراءة ملف الإكسل وتحويله إلى جدول بيانات (DataFrame)
    df = pd.read_excel(uploaded_file)
    
    st.success("✅ تم تحميل الملف وقراءة الأعمدة بنجاح!")
    
    # استخراج أسماء الأعمدة من الملف
    all_columns = df.columns.tolist()
    
    # 1. قسم اختيار الأعمدة المراد عرضها
    st.subheader("📋 1. اختر الأعمدة التي تريد ظهورها في الجدول:")
    selected_columns = st.multiselect(
        "يمكنك تحديد أعمدة معينة أو تركها فارغة لعرض الملف كاملاً:", 
        options=all_columns, 
        default=all_columns
    )
    
    # 2. قسم التصفية الذكية بناءً على قيم الأعمدة
    st.subheader("🎯 2. تصفية البيانات (Filter):")
    
    # تصفية أولية تبدأ بالملف كاملاً
    filtered_df = df.copy()
    
    # سننشئ صفوفاً تحتوي على قوائم تصفية للأعمدة النصية أو التصنيفية كمثال
    col_selectors = st.columns(min(len(all_columns), 3)) # تقسيم القوائم إلى 3 أعمدة في الواجهة
    
    for i, column in enumerate(all_columns[:3]): # لنأخذ أول 3 أعمدة للتصفية كمثال تلقائي
        unique_values = df[column].dropna().unique().tolist()
        # إذا كانت القيم فريدة وقليلة (تصلح لتكون قائمة خيارات)
        if len(unique_values) < 100: 
            with col_selectors[i % 3]:
                selected_values = st.multiselect(f"تصفية حسب ({column}):", options=unique_values)
                if selected_values:
                    filtered_df = filtered_df[filtered_df[column].isin(selected_values)]

    # 3. عرض النتائج النهائية
    st.subheader("📊 3. البيانات الناتجة:")
    
    # تطبيق اختيار الأعمدة التي حددها المستخدم
    if selected_columns:
        final_display_df = filtered_df[selected_columns]
    else:
        final_display_df = filtered_df
        
    # عرض الجدول النهائي مع أيقونة توضح عدد السجلات المتبقية
    st.metric(label="🔢 عدد السجلات المطابقة لبحثك", value=len(final_display_df))
    st.dataframe(final_display_df, use_container_width=True)

else:
    st.info("💡 يرجى رفع ملف إكسل من القائمة أعلاه لبدء استعراض البيانات.")
