import type {ReactNode} from 'react';
import {createContext,useContext,useEffect,useState} from 'react';
import {createClient,type Session,type SupabaseClient} from '@supabase/supabase-js';

export type Identity={user_id:string;session_id:string;display_name:string;smart_name:string;smart_alias:string;permissions:string[];privacy_state:string};

const SUPABASE_URL=import.meta.env.VITE_SUPABASE_URL||'https://dahisasgpfvziswqvmvm.supabase.co';
const SUPABASE_KEY=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY||'sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue';
const supabase:SupabaseClient=createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});

const fallback:Identity={user_id:'local-preview',session_id:'local-preview',display_name:'Preview',smart_name:'Preview User',smart_alias:'preview',permissions:['personal'],privacy_state:'PRIVATE BY DEFAULT'};

function identityFromSession(session:Session):Identity{
  const metadata=session.user.user_metadata||{};
  const displayName=typeof metadata.display_name==='string'?metadata.display_name:typeof metadata.full_name==='string'?metadata.full_name:'NayaNET Member';
  const smartName=typeof metadata.smart_name==='string'?metadata.smart_name:displayName;
  const smartAlias=typeof metadata.smart_alias==='string'?metadata.smart_alias:'member';
  const permissions=Array.isArray(metadata.permissions)?metadata.permissions.filter((value):value is string=>typeof value==='string'):['personal'];
  return {user_id:session.user.id,session_id:session.access_token,display_name:displayName,smart_name:smartName,smart_alias:smartAlias,permissions,privacy_state:'PRIVATE BY DEFAULT'};
}

export const IdentityContext=createContext<Identity>(fallback);
export function useIdentity(){return useContext(IdentityContext)}

export function IdentityProvider({children}:{children:ReactNode}){
  const [identity,setIdentity]=useState<Identity>(fallback);
  useEffect(()=>{
    let alive=true;
    supabase.auth.getSession().then(({data})=>{if(alive&&data.session)setIdentity(identityFromSession(data.session));});
    const {data:{subscription}}=supabase.auth.onAuthStateChange((_event,session)=>{if(alive)setIdentity(session?identityFromSession(session):fallback);});
    return()=>{alive=false;subscription.unsubscribe()};
  },[]);
  return <IdentityContext.Provider value={identity}>{children}</IdentityContext.Provider>;
}

export {supabase};
